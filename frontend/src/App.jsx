import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:8000';

export default function App() {
  const [longUrl, setLongUrl] = useState('');
  const [createdResult, setCreatedResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Analytics state
  const [analyticsCode, setAnalyticsCode] = useState('');
  const [analyticsData, setAnalyticsData] = useState(null);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [analyticsError, setAnalyticsError] = useState('');

  const handleShorten = async (e) => {
    e.preventDefault();
    if (!longUrl.trim()) return;
    
    setLoading(true);
    setError('');
    setCreatedResult(null);

    try {
      const res = await fetch(`${API_BASE}/shorten`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ original_url: longUrl }),
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Failed to shorten URL');
      }

      const data = await res.json();
      setCreatedResult(data);
      setLongUrl('');
      // Auto fetch analytics for newly created code
      fetchAnalytics(data.short_code);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalytics = async (code) => {
    const targetCode = code || analyticsCode;
    if (!targetCode.trim()) return;

    setAnalyticsLoading(true);
    setAnalyticsError('');

    try {
      const res = await fetch(`${API_BASE}/analytics/${targetCode.trim()}`);
      if (!res.ok) {
        if (res.status === 404) throw new Error('Short link not found');
        throw new Error('Failed to fetch analytics');
      }
      const data = await res.json();
      setAnalyticsData(data);
      setAnalyticsCode(targetCode.trim());
    } catch (err) {
      setAnalyticsError(err.message);
      setAnalyticsData(null);
    } finally {
      setAnalyticsLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="container">
      <header>
        <h1>🔗 High-Speed URL Shortener</h1>
        <p>Built with FastAPI, PostgreSQL, Redis & React · ACM VNIT Mentorship Track</p>
      </header>

      {/* SECTION 1: SHORTEN URL FORM */}
      <div className="card">
        <h2>Shorten a Long Link</h2>
        <form onSubmit={handleShorten} className="input-group">
          <input
            type="text"
            placeholder="Paste a long URL here (e.g., https://example.com/very/long/path)..."
            value={longUrl}
            onChange={(e) => setLongUrl(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Shortening...' : 'Shorten URL'}
          </button>
        </form>

        {error && <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{error}</p>}

        {createdResult && (
          <div className="result-box">
            <div>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Your Short Link:</p>
              <a href={createdResult.short_url} target="_blank" rel="noopener noreferrer">
                {createdResult.short_url}
              </a>
            </div>
            <button onClick={() => copyToClipboard(createdResult.short_url)}>
              Copy Link
            </button>
          </div>
        )}
      </div>

      {/* SECTION 2: ANALYTICS DASHBOARD */}
      <div className="card">
        <h2>Analytics Dashboard</h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem' }}>
          Inspect total clicks and recent visitor activity for any short code
        </p>

        <div className="input-group">
          <input
            type="text"
            placeholder="Enter short code (e.g. 1)..."
            value={analyticsCode}
            onChange={(e) => setAnalyticsCode(e.target.value)}
          />
          <button onClick={() => fetchAnalytics()} disabled={analyticsLoading}>
            {analyticsLoading ? 'Fetching...' : 'View Analytics'}
          </button>
        </div>

        {analyticsError && (
          <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{analyticsError}</p>
        )}

        {analyticsData && (
          <div style={{ marginTop: '2rem' }}>
            <div className="stats-grid">
              <div className="stat-card">
                <span className="badge">Total Traffic</span>
                <div className="stat-number">{analyticsData.total_clicks}</div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>Total Recorded Clicks</p>
              </div>

              <div className="stat-card">
                <span className="badge">Short Code</span>
                <div className="stat-number" style={{ color: 'var(--primary-accent)' }}>
                  {analyticsData.short_code}
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>Base62 Identifier</p>
              </div>

              <div className="stat-card" style={{ gridColumn: 'span 2' }}>
                <span className="badge">Destination URL</span>
                <p style={{ wordBreak: 'break-all', marginTop: '0.75rem', fontWeight: 500 }}>
                  {analyticsData.original_url}
                </p>
              </div>
            </div>

            <h3>Recent Visitor Activity (Last 20)</h3>
            {analyticsData.recent_clicks.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>
                No clicks recorded yet. Click your short link to see live background analytics!
              </p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Timestamp</th>
                    <th>IP Address</th>
                    <th>User Agent</th>
                  </tr>
                </thead>
                <tbody>
                  {analyticsData.recent_clicks.map((c, idx) => (
                    <tr key={c.id || idx}>
                      <td>{idx + 1}</td>
                      <td>{new Date(c.clicked_at).toLocaleString()}</td>
                      <td><span className="badge">{c.ip_address || '127.0.0.1'}</span></td>
                      <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {c.user_agent ? c.user_agent.substring(0, 45) + '...' : 'Browser/cURL'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
