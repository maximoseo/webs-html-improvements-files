from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'
PLAN_DOC = Path('/home/seoadmin/.hermes/cache/documents/doc_57e0d0a2c4f5_hermes-dashboard-missing-features-plan.md')


def html():
    return INDEX_HTML.read_text(encoding='utf-8')


def test_uploaded_missing_features_plan_is_available_and_mentions_all_features():
    assert PLAN_DOC.exists()
    text = PLAN_DOC.read_text(encoding='utf-8')
    for feature in [
        'Client Overview Home Page',
        'A/B Testing & Version Comparison',
        'Agent Observability & Trace Viewer',
        'Automated Client Reporting',
        'Template Gallery & Favorites',
        'Notification Center & Alerts',
        'Batch Operations & Bulk Actions',
        'Search & Global Filter System',
        'Audit Log & Change History',
        'Quick Actions & Keyboard Shortcuts',
        'Cost Tracker & Budget Alerts',
        'Collaboration & Team Notes',
        'Mobile-Responsive Progressive Web App',
        'Data Export Hub',
        'Scheduled Pipeline Runs',
    ]:
        assert feature in text


def test_productivity_hub_tab_and_page_are_additive_and_unique():
    s = html()
    assert 'MISSING_FEATURES_PRODUCTIVITY_HUB_2026_04_27' in s
    assert len(re.findall(r'<button[^>]*id="tab-productivity-hub"', s)) == 1
    assert len(re.findall(r'<button[^>]*data-testid="tab-productivity-hub"', s)) == 1
    assert len(re.findall(r'<button[^>]*data-testid="mobile-nav-productivity-hub"', s)) == 1
    assert len(re.findall(r'<div[^>]*id="page-productivity-hub"', s)) == 1
    assert "showPage('productivity-hub')" in s
    assert "var productivityHubPage = document.getElementById('page-productivity-hub')" in s
    assert "productivityHubPage.style.display = isProductivityHub ? 'block' : 'none'" in s


def test_productivity_hub_covers_all_15_uploaded_features_with_statuses():
    s = html()
    for slug in [
        'client-overview', 'ab-testing', 'agent-traces', 'client-reports', 'template-gallery',
        'notifications', 'batch-operations', 'global-search', 'audit-log', 'quick-actions',
        'cost-tracker', 'team-notes', 'pwa-mobile', 'export-hub', 'scheduled-runs'
    ]:
        assert f'data-roadmap-feature="{slug}"' in s
    for marker in [
        'Feature flags', 'Enabled now', 'Planned next', 'No n8n workflow modification',
        'Additive only', 'Rollback: disable feature flag'
    ]:
        assert marker in s


def test_quick_wins_have_safe_client_side_functions_and_no_backend_route_changes():
    s = html()
    for fn in [
        'window.mfOpenCommandPalette',
        'window.mfCloseCommandPalette',
        'window.mfRenderNotifications',
        'window.mfRenderCostTracker',
        'window.mfRecordAuditEvent',
        'window.mfExportRoadmapJson',
        'window.mfToggleFeatureFlag',
    ]:
        assert fn in s
    assert 'MISSING_FEATURES_PRODUCTIVITY_HUB_STYLE_2026_04_27' in s
    assert 'MISSING_FEATURES_PRODUCTIVITY_HUB_JS_2026_04_27' in s
    # This first implementation must stay client-side/additive and must not add risky n8n mutation calls.
    block = s[s.find('MISSING_FEATURES_PRODUCTIVITY_HUB_JS_2026_04_27'):]
    assert 'n8n' not in block.lower() or 'No n8n workflow modification' in block
    assert 'deleteWorkflow' not in block
    assert 'createWorkflow' not in block


def test_command_palette_shortcuts_are_guarded_for_inputs():
    s = html()
    assert "ev.target.closest('input,textarea,select,[contenteditable=\"true\"]')" in s
    assert "ev.key.toLowerCase()==='k'" in s
    assert "ev.key==='?'" in s
    assert 'data-testid="missing-features-command-palette"' in s
