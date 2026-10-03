import { useState, useEffect, useRef } from 'react';
import './ResearchPapers.css';

// ═══════════════════════════════════════════════════════════════
// CLIENT-SIDE FUZZY MATCHING (mirrors Python rapidfuzz logic)
// ═══════════════════════════════════════════════════════════════

function normalizeTitle(title) {
  if (!title) return '';
  let t = title.toLowerCase().trim();
  t = t.replace(/\s*\(\d+\)\s*$/, '');
  t = t.replace(/[^\w\s]/g, ' ');
  t = t.replace(/\s+/g, ' ').trim();
  return t;
}

/** Levenshtein distance (Wagner-Fischer algorithm) */
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  if (m === 0) return n;
  if (n === 0) return m;
  // Use single-row optimization for memory
  let prev = Array.from({ length: n + 1 }, (_, i) => i);
  let curr = new Array(n + 1);
  for (let i = 1; i <= m; i++) {
    curr[0] = i;
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      curr[j] = Math.min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost);
    }
    [prev, curr] = [curr, prev];
  }
  return prev[n];
}

/** fuzz.ratio — simple ratio */
function fuzzyRatio(a, b) {
  if (a === b) return 100;
  if (!a || !b) return 0;
  const maxLen = Math.max(a.length, b.length);
  if (maxLen === 0) return 100;
  const dist = levenshtein(a, b);
  return ((maxLen - dist) / maxLen) * 100;
}

/** fuzz.token_sort_ratio — sort tokens then compare */
function tokenSortRatio(a, b) {
  const sortedA = a.split(/\s+/).sort().join(' ');
  const sortedB = b.split(/\s+/).sort().join(' ');
  return fuzzyRatio(sortedA, sortedB);
}

/** fuzz.token_set_ratio — set intersection/difference approach */
function tokenSetRatio(a, b) {
  const setA = new Set(a.split(/\s+/));
  const setB = new Set(b.split(/\s+/));
  const intersection = [...setA].filter(t => setB.has(t));
  const diffA = [...setA].filter(t => !setB.has(t));
  const diffB = [...setB].filter(t => !setA.has(t));

  const sorted_sect = intersection.sort().join(' ');
  const combined_a = [sorted_sect, ...diffA.sort()].join(' ').trim();
  const combined_b = [sorted_sect, ...diffB.sort()].join(' ').trim();

  return Math.max(
    fuzzyRatio(sorted_sect, combined_a),
    fuzzyRatio(sorted_sect, combined_b),
    fuzzyRatio(combined_a, combined_b)
  );
}

/** fuzz.partial_ratio — best partial substring match */
function partialRatio(a, b) {
  if (a.length > b.length) [a, b] = [b, a]; // a is shorter
  if (a.length === 0) return 0;
  let best = 0;
  // Slide shorter string along longer string
  for (let i = 0; i <= b.length - a.length; i++) {
    const sub = b.substring(i, i + a.length);
    const score = fuzzyRatio(a, sub);
    if (score > best) best = score;
    if (best === 100) return 100;
  }
  return best;
}

/**
 * Composite similarity — mirrors Python backend:
 *   composite = ratio * 0.30 + token_sort * 0.30 + token_set * 0.20 + partial * 0.20
 */
function calculateSimilarity(title1, title2) {
  const t1 = normalizeTitle(title1);
  const t2 = normalizeTitle(title2);

  if (t1 === t2) {
    return { ratio: 100, token_sort: 100, token_set: 100, partial: 100, composite: 100 };
  }

  const ratio = fuzzyRatio(t1, t2);
  const token_sort = tokenSortRatio(t1, t2);
  const token_set = tokenSetRatio(t1, t2);
  const partial = partialRatio(t1, t2);
  const composite = ratio * 0.30 + token_sort * 0.30 + token_set * 0.20 + partial * 0.20;

  return {
    ratio: Math.round(ratio * 100) / 100,
    token_sort: Math.round(token_sort * 100) / 100,
    token_set: Math.round(token_set * 100) / 100,
    partial: Math.round(partial * 100) / 100,
    composite: Math.round(composite * 10) / 10,
  };
}

// ═══════════════════════════════════════════════════════════════
// BACKEND API (only for Upload — requires local Flask)
// ═══════════════════════════════════════════════════════════════
async function apiFetch(endpoint, options = {}) {
  try {
    const res = await fetch(endpoint, options);
    if (res.ok || res.status < 500) return await res.json();
  } catch { /* proxy failed */ }
  const directUrl = `http://localhost:5000${endpoint}`;
  const res = await fetch(directUrl, options);
  return await res.json();
}

// Thresholds (same as Python backend)
const EXACT_MATCH_THRESHOLD = 95;
const POTENTIAL_MATCH_THRESHOLD = 70;

// SVG Icons
const UploadIcon = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <polyline points="14 2 14 8 20 8" />
    <path d="M12 18v-6" />
    <path d="m9 15 3-3 3 3" />
  </svg>
);

const SearchIcon = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" />
    <path d="m21 21-4.3-4.3" />
  </svg>
);

const DatabaseIcon = ({ size = 18 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3" />
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
    <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" />
  </svg>
);

export default function ResearchPapers({ onBack }) {
  const [activeTab, setActiveTab] = useState('search'); // 'upload' | 'search' | 'browse'
  const [dbPapers, setDbPapers] = useState([]);
  const [dbLoaded, setDbLoaded] = useState(false);
  const [dbError, setDbError] = useState(false);
  const [toast, setToast] = useState(null);

  // Upload Tab States
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [filterType, setFilterType] = useState('all');
  const [approvedMap, setApprovedMap] = useState({});
  const [rejectedMap, setRejectedMap] = useState({});
  const fileInputRef = useRef(null);

  // Title Search States
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResult, setSearchResult] = useState(null);

  // Browse DB States
  const [browseQuery, setBrowseQuery] = useState('');

  // Load papers database (static JSON) on mount
  useEffect(() => {
    loadPapersDb();
  }, []);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const loadPapersDb = async () => {
    try {
      const res = await fetch(`${import.meta.env.BASE_URL}papers_db.json`);
      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();
      if (data && data.papers) {
        setDbPapers(data.papers);
        setDbLoaded(true);
      } else {
        throw new Error('Invalid format');
      }
    } catch (err) {
      console.error('Failed to load papers_db.json:', err);
      setDbError(true);
      // Fallback: try backend API
      try {
        const data = await apiFetch('/api/papers');
        if (data && data.papers) {
          setDbPapers(data.papers);
          setDbLoaded(true);
          setDbError(false);
        }
      } catch {
        console.warn('Backend also unavailable');
      }
    }
  };

  const totalPapers = dbPapers.length || 137;

  // Switch Tab
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // ───────────────────────────────────────────────
  // FILE UPLOAD (requires local Flask backend)
  // ───────────────────────────────────────────────
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files).filter(f => f.name.toLowerCase().endsWith('.pdf'));
    if (files.length === 0) {
      showToast('Please select valid PDF files only', 'error');
      return;
    }
    setSelectedFiles(files);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files).filter(f => f.name.toLowerCase().endsWith('.pdf'));
    if (files.length === 0) {
      showToast('Please drop PDF files only', 'error');
      return;
    }
    setSelectedFiles(files);
  };

  const runAnalysis = async () => {
    if (selectedFiles.length === 0) return;
    setIsUploading(true);
    setAnalysisResults(null);

    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append('papers', file);
    });

    try {
      const data = await apiFetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (data.error) {
        showToast(data.error, 'error');
        return;
      }

      setAnalysisResults(data);
      showToast(`Analyzed ${data.results.length} papers successfully!`);
    } catch (err) {
      showToast('Connection error: Ensure Flask backend is running on port 5000', 'error');
    } finally {
      setIsUploading(false);
    }
  };

  const handleApprove = async (paper) => {
    const filename = paper.saved_as || paper.filename;
    try {
      const res = await apiFetch('/api/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename }),
      });
      if (res.success) {
        setApprovedMap(prev => ({ ...prev, [paper.filename]: true }));
        showToast(`Approved: "${paper.title || paper.filename}"`);
      } else {
        showToast(res.error || 'Failed to approve', 'error');
      }
    } catch {
      showToast('Error approving paper', 'error');
    }
  };

  const handleReject = async (paper) => {
    const filename = paper.saved_as || paper.filename;
    try {
      const res = await apiFetch('/api/reject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename }),
      });
      if (res.success) {
        setRejectedMap(prev => ({ ...prev, [paper.filename]: true }));
        showToast(`Dismissed: "${paper.filename}"`, 'info');
      }
    } catch {
      showToast('Error rejecting paper', 'error');
    }
  };

  const handleApproveAllNew = async () => {
    if (!analysisResults) return;
    const newPapers = analysisResults.results.filter(
      r => r.status === 'new' && !approvedMap[r.filename] && !rejectedMap[r.filename]
    );
    if (newPapers.length === 0) {
      showToast('No unapproved new papers to add', 'info');
      return;
    }
    const filenames = newPapers.map(p => p.saved_as || p.filename);
    try {
      const res = await apiFetch('/api/approve-all-new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filenames }),
      });
      if (res.success) {
        const updated = { ...approvedMap };
        newPapers.forEach(p => { updated[p.filename] = true; });
        setApprovedMap(updated);
        showToast(`Approved all ${res.approved_count} new papers!`);
      }
    } catch {
      showToast('Error approving papers', 'error');
    }
  };

  // ───────────────────────────────────────────────
  // SEARCH BY TITLE (client-side fuzzy matching)
  // ───────────────────────────────────────────────
  const handleTitleSearch = (e) => {
    if (e) e.preventDefault();
    const query = searchQuery.trim();
    if (!query || query.length < 3) {
      showToast('Please enter at least 3 characters', 'error');
      return;
    }

    if (!dbLoaded || dbPapers.length === 0) {
      showToast('Papers database not loaded yet', 'error');
      return;
    }

    setIsSearching(true);
    setSearchResult(null);

    // Run matching in a setTimeout to avoid UI freeze
    setTimeout(() => {
      const matches = [];
      for (const existing of dbPapers) {
        const sim = calculateSimilarity(query, existing.title);
        if (sim.composite >= 30) {
          matches.push({
            title: existing.title,
            filename: existing.filename,
            score: sim.composite,
            status: sim.composite >= EXACT_MATCH_THRESHOLD
              ? 'duplicate'
              : sim.composite >= POTENTIAL_MATCH_THRESHOLD
                ? 'potential'
                : 'low',
          });
        }
      }

      matches.sort((a, b) => b.score - a.score);

      let verdict, verdict_text;
      if (matches.length > 0 && matches[0].score >= EXACT_MATCH_THRESHOLD) {
        verdict = 'duplicate';
        verdict_text = 'This paper likely already exists in the database';
      } else if (matches.length > 0 && matches[0].score >= POTENTIAL_MATCH_THRESHOLD) {
        verdict = 'potential';
        verdict_text = 'Similar papers found — manual review recommended';
      } else {
        verdict = 'new';
        verdict_text = 'No matching papers found — this appears to be new';
      }

      setSearchResult({
        query,
        verdict,
        verdict_text,
        top_matches: matches.slice(0, 3),
        total_compared: dbPapers.length,
      });
      setIsSearching(false);
    }, 50);
  };

  // Filtered analysis results
  const filteredResults = analysisResults?.results.filter((paper) => {
    if (filterType === 'all') return true;
    return paper.status === filterType;
  }) || [];

  // Filtered DB papers for browse tab
  const filteredDbPapers = dbPapers.filter((p) => {
    const q = browseQuery.toLowerCase();
    return p.title.toLowerCase().includes(q) || p.filename.toLowerCase().includes(q);
  });

  return (
    <div className="research-page">
      <div className="container research-container">
        
        {/* Top bar */}
        <div className="research-topbar">
          <button className="back-btn" onClick={onBack}>
            <span>←</span> Back to Main Page
          </button>

          <div className="db-pill">
            <span className="dot" style={{ width: 8, height: 8, borderRadius: '50%', background: dbLoaded ? 'var(--accent)' : '#F87171' }}></span>
            Indexed Database: <span className="num">{totalPapers} Unique Papers</span>
            {dbLoaded && <span style={{ fontSize: '0.7rem', color: '#4ADE80', marginLeft: '0.4rem' }}>● Online</span>}
          </div>
        </div>

        {/* Page Header */}
        <div className="research-header">
          <div className="section-badge">RESEARCH & DEDUPLICATION</div>
          <h1>Paper Deduplication System</h1>
          <p>
            Automated multi-stage comparison engine. Ingest newly discovered papers, 
            detect exact or semantic duplicates, and expand our graduation project knowledge base safely.
          </p>
        </div>

        {/* Mode Tabs */}
        <div className="research-tabs">
          <button
            className={`research-tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => handleTabChange('upload')}
          >
            <UploadIcon size={18} />
            <span>Upload PDFs</span>
          </button>
          <button
            className={`research-tab-btn ${activeTab === 'search' ? 'active' : ''}`}
            onClick={() => handleTabChange('search')}
          >
            <SearchIcon size={18} />
            <span>Search Title (Top 3)</span>
          </button>
          <button
            className={`research-tab-btn ${activeTab === 'browse' ? 'active' : ''}`}
            onClick={() => handleTabChange('browse')}
          >
            <DatabaseIcon size={18} />
            <span>Browse Database ({totalPapers})</span>
          </button>
        </div>

        {/* ========================================================
            TAB 1: UPLOAD & VERIFY PDFS
            ======================================================== */}
        {activeTab === 'upload' && (
          <div className="upload-view">
            {/* Backend requirement notice */}
            <div className="backend-notice">
              <div className="backend-notice-icon">⚙️</div>
              <div>
                <strong>Local Backend Required</strong>
                <p>
                  PDF upload and analysis requires the Flask backend running locally on port 5000.
                  Run <code>python Researching/app.py</code> from the project root to start it.
                </p>
              </div>
            </div>

            {/* Dropzone */}
            <div
              className={`upload-dropzone ${isDragging ? 'dragging' : ''}`}
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept=".pdf"
                onChange={handleFileChange}
              />
              <div className="dropzone-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
              </div>
              <h3>Drop your PDF Research Papers here</h3>
              <p>or click to browse from device • Supports bulk multi-file upload</p>
            </div>

            {/* Selected files preview */}
            {selectedFiles.length > 0 && !isUploading && (
              <div className="selected-files-bar">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>
                    {selectedFiles.length} {selectedFiles.length === 1 ? 'file' : 'files'} selected
                  </span>
                  <div className="file-tags">
                    {selectedFiles.map((f, i) => (
                      <span key={i} className="file-tag">
                        📎 {f.name}
                      </span>
                    ))}
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.6rem' }}>
                  <button
                    className="btn btn-primary"
                    onClick={runAnalysis}
                    disabled={isUploading}
                  >
                    ⚡ Run Deduplication Analysis
                  </button>
                  <button
                    className="btn btn-outline"
                    onClick={() => { setSelectedFiles([]); setAnalysisResults(null); }}
                  >
                    Clear
                  </button>
                </div>
              </div>
            )}

            {/* Loading Spinner */}
            {isUploading && (
              <div style={{ textAlign: 'center', padding: '3rem' }}>
                <div className="spinner-ring"></div>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '0.4rem' }}>
                  Analyzing papers against database...
                </h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                  Extracting titles, computing hashes, and performing fuzzy & token matching
                </p>
              </div>
            )}

            {/* Analysis Results */}
            {analysisResults && !isUploading && (
              <div className="results-container">
                {/* Stats Summary Bar */}
                <div className="stats-summary-grid">
                  <div className="stat-metric-card stat-total">
                    <div className="stat-val">{analysisResults.summary.total}</div>
                    <div className="stat-name">Processed</div>
                  </div>
                  <div className="stat-metric-card stat-dup">
                    <div className="stat-val">{analysisResults.summary.duplicates}</div>
                    <div className="stat-name">Duplicates (≥95%)</div>
                  </div>
                  <div className="stat-metric-card stat-pot">
                    <div className="stat-val">{analysisResults.summary.potential}</div>
                    <div className="stat-name">Potential (70-94%)</div>
                  </div>
                  <div className="stat-metric-card stat-new">
                    <div className="stat-val">{analysisResults.summary.new}</div>
                    <div className="stat-name">New Papers (&lt;70%)</div>
                  </div>
                </div>

                {/* Filter and Bulk Action Controls */}
                <div className="results-controls">
                  <div className="filter-group">
                    <button
                      className={`filter-btn ${filterType === 'all' ? 'active' : ''}`}
                      onClick={() => setFilterType('all')}
                    >
                      All ({analysisResults.results.length})
                    </button>
                    <button
                      className={`filter-btn ${filterType === 'new' ? 'active' : ''}`}
                      onClick={() => setFilterType('new')}
                    >
                      🟢 New ({analysisResults.summary.new})
                    </button>
                    <button
                      className={`filter-btn ${filterType === 'potential' ? 'active' : ''}`}
                      onClick={() => setFilterType('potential')}
                    >
                      🟡 Potential ({analysisResults.summary.potential})
                    </button>
                    <button
                      className={`filter-btn ${filterType === 'duplicate' ? 'active' : ''}`}
                      onClick={() => setFilterType('duplicate')}
                    >
                      🔴 Duplicates ({analysisResults.summary.duplicates})
                    </button>
                  </div>

                  <div style={{ display: 'flex', gap: '0.6rem' }}>
                    {analysisResults.summary.new > 0 && (
                      <button className="btn btn-primary" onClick={handleApproveAllNew}>
                        ✓ Approve All New Papers
                      </button>
                    )}
                    <button
                      className="btn btn-outline"
                      onClick={() => {
                        setAnalysisResults(null);
                        setSelectedFiles([]);
                      }}
                    >
                      New Batch
                    </button>
                  </div>
                </div>

                {/* Paper Cards List */}
                <div className="paper-cards-list">
                  {filteredResults.map((paper, idx) => {
                    const isApproved = approvedMap[paper.filename];
                    const isRejected = rejectedMap[paper.filename];
                    const score = paper.score || 0;
                    const scoreColor =
                      score >= 95 ? '#F87171' : score >= 70 ? '#FACC15' : '#4ADE80';

                    return (
                      <div
                        key={idx}
                        className={`paper-item-card is-${paper.status} ${
                          isApproved ? 'is-approved' : ''
                        } ${isRejected ? 'is-rejected' : ''}`}
                      >
                        {/* Status Icon Column */}
                        <div>
                          <span
                            className={`badge-status ${
                              paper.status === 'duplicate'
                                ? 'dup'
                                : paper.status === 'potential'
                                ? 'pot'
                                : 'new'
                            }`}
                          >
                            {paper.status === 'duplicate' && '🔴 Duplicate'}
                            {paper.status === 'potential' && '🟡 Review'}
                            {paper.status === 'new' && '🟢 New Paper'}
                          </span>
                        </div>

                        {/* Paper Details */}
                        <div className="paper-main-content">
                          <h4>{paper.title || 'Untitled Document'}</h4>
                          <div className="file-name">📎 {paper.filename}</div>

                          {/* Match Details */}
                          {paper.matched_title && (
                            <div className="match-box">
                              <div className="match-box-header">
                                <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>
                                  Closest Database Match:
                                </span>
                                <span style={{ color: scoreColor, fontWeight: 700 }}>
                                  {score}% Similarity
                                </span>
                              </div>
                              <div className="match-target-title">
                                {paper.matched_title}
                              </div>
                              <div className="match-target-file">
                                Found in: {paper.matched_filename}
                              </div>

                              {/* Similarity bar */}
                              <div className="score-pill-container">
                                <div className="score-progress-track">
                                  <div
                                    className="score-progress-fill"
                                    style={{
                                      width: `${score}%`,
                                      background: scoreColor,
                                    }}
                                  ></div>
                                </div>
                                <span className="score-val" style={{ color: scoreColor }}>
                                  {score}%
                                </span>
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Actions */}
                        <div className="paper-actions-col">
                          {!isApproved && !isRejected && (
                            <>
                              <button
                                className="btn btn-primary"
                                style={{ padding: '0.55rem 1rem', fontSize: '0.8rem' }}
                                onClick={() => handleApprove(paper)}
                              >
                                Approve & Add
                              </button>
                              <button
                                className="btn btn-outline"
                                style={{ padding: '0.55rem 1rem', fontSize: '0.8rem', color: '#F87171' }}
                                onClick={() => handleReject(paper)}
                              >
                                Dismiss
                              </button>
                            </>
                          )}
                          {isApproved && (
                            <span style={{ color: '#4ADE80', fontWeight: 600, fontSize: '0.85rem' }}>
                              ✓ In Database
                            </span>
                          )}
                          {isRejected && (
                            <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                              Dismissed
                            </span>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ========================================================
            TAB 2: SEARCH TITLE (TOP 3 MATCHES) — CLIENT-SIDE
            ======================================================== */}
        {activeTab === 'search' && (
          <div className="search-card-container">
            <div className="search-box-card">
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <SearchIcon size={22} />
                <span>Compare Paper by Title</span>
              </h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                Type or paste a candidate paper's title to search our {totalPapers} unique papers and see the <strong>Top 3</strong> closest matches.
              </p>

              <form onSubmit={handleTitleSearch} className="search-input-group">
                <input
                  type="text"
                  placeholder="e.g. Obstacle Detection for Visually Impaired Navigation..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={isSearching || !dbLoaded}
                >
                  {isSearching ? 'Comparing...' : !dbLoaded ? 'Loading DB...' : 'Compare Title'}
                </button>
              </form>

              {/* Sample queries */}
              <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Try example:</span>
                <button
                  type="button"
                  className="file-tag"
                  style={{ cursor: 'pointer' }}
                  onClick={() => setSearchQuery('Obstacle Detection for Visually Impaired')}
                >
                  Obstacle Detection
                </button>
                <button
                  type="button"
                  className="file-tag"
                  style={{ cursor: 'pointer' }}
                  onClick={() => setSearchQuery('Tactile Haptic Belt Navigation')}
                >
                  Tactile Haptic Belt
                </button>
                <button
                  type="button"
                  className="file-tag"
                  style={{ cursor: 'pointer' }}
                  onClick={() => setSearchQuery('Autonomous Drone Vision for Blind People')}
                >
                  Autonomous Drone Vision
                </button>
              </div>

              {/* Database status indicator */}
              {dbError && !dbLoaded && (
                <div style={{ marginTop: '1rem', padding: '0.8rem 1rem', background: 'rgba(248,113,113,0.1)', borderRadius: '8px', border: '1px solid rgba(248,113,113,0.3)', fontSize: '0.85rem', color: '#F87171' }}>
                  ⚠️ Could not load papers database. Make sure <code>papers_db.json</code> is in the <code>public/</code> folder.
                </div>
              )}

              {/* Verdict Banner */}
              {searchResult && (
                <>
                  <div className={`verdict-banner v-${searchResult.verdict}`}>
                    <div className="verdict-icon-lg">
                      {searchResult.verdict === 'duplicate' && '🔴'}
                      {searchResult.verdict === 'potential' && '🟡'}
                      {searchResult.verdict === 'new' && '🟢'}
                    </div>
                    <div className="verdict-text-box">
                      <h4>{searchResult.verdict_text}</h4>
                      <p>Compared query against all {searchResult.total_compared} papers in database</p>
                    </div>
                  </div>

                  {/* Top 3 Matches */}
                  <div className="top-matches-heading">
                    <h4>Top {searchResult.top_matches?.length || 0} Matches</h4>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      Ranked by multi-metric composite similarity
                    </span>
                  </div>

                  {searchResult.top_matches && searchResult.top_matches.length > 0 ? (
                    searchResult.top_matches.map((m, idx) => {
                      const scoreColor =
                        m.score >= 95 ? '#F87171' : m.score >= 70 ? '#FACC15' : '#4ADE80';

                      return (
                        <div key={idx} className="top-match-item">
                          <div className="rank-badge">#{idx + 1}</div>

                          <div className="top-match-info">
                            <div className="top-match-title">{m.title}</div>
                            <div className="top-match-meta">📎 {m.filename}</div>

                            <div className="score-pill-container" style={{ maxWidth: 300, marginTop: '0.4rem' }}>
                              <div className="score-progress-track">
                                <div
                                  className="score-progress-fill"
                                  style={{ width: `${m.score}%`, background: scoreColor }}
                                ></div>
                              </div>
                              <span className="score-val" style={{ color: scoreColor }}>
                                {m.score}%
                              </span>
                            </div>
                          </div>

                          <div>
                            <span
                              className={`badge-status ${
                                m.status === 'duplicate'
                                  ? 'dup'
                                  : m.status === 'potential'
                                  ? 'pot'
                                  : 'new'
                              }`}
                            >
                              {m.status === 'duplicate' ? 'Match' : m.status === 'potential' ? 'Similar' : 'Low'}
                            </span>
                          </div>
                        </div>
                      );
                    })
                  ) : (
                    <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>
                      No matching records found in the database.
                    </p>
                  )}
                </>
              )}
            </div>
          </div>
        )}

        {/* ========================================================
            TAB 3: BROWSE ALL UNIQUE PAPERS — CLIENT-SIDE
            ======================================================== */}
        {activeTab === 'browse' && (
          <div className="browse-papers-box">
            <div className="browse-search-bar">
              <input
                type="text"
                placeholder={`Search across all ${totalPapers} indexed papers by title or filename...`}
                value={browseQuery}
                onChange={(e) => setBrowseQuery(e.target.value)}
              />
            </div>

            {!dbLoaded ? (
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                {dbError ? (
                  <p style={{ color: '#F87171' }}>⚠️ Failed to load papers database</p>
                ) : (
                  <>
                    <div className="spinner-ring"></div>
                    <p>Loading database papers...</p>
                  </>
                )}
              </div>
            ) : (
              <div className="papers-table-wrap">
                <table className="papers-table">
                  <thead>
                    <tr>
                      <th style={{ width: 60 }}>#</th>
                      <th>Paper Title</th>
                      <th style={{ width: 220 }}>File Name</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredDbPapers.map((paper, idx) => (
                      <tr key={idx}>
                        <td style={{ color: 'var(--text-muted)' }}>{idx + 1}</td>
                        <td style={{ fontWeight: 500 }}>{paper.title}</td>
                        <td style={{ color: 'var(--text-muted)', fontFamily: 'monospace', fontSize: '0.8rem' }}>
                          {paper.filename}
                        </td>
                      </tr>
                    ))}
                    {filteredDbPapers.length === 0 && (
                      <tr>
                        <td colSpan={3} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                          No papers matching "{browseQuery}"
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

      </div>

      {/* Floating Toast Notification */}
      {toast && (
        <div className={`toast-notice ${toast.type}`}>
          <span>{toast.type === 'error' ? '⚠️' : '✓'}</span>
          <span>{toast.message}</span>
        </div>
      )}
    </div>
  );
}
