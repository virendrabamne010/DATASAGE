import streamlit as st
import os
import json
from pathlib import Path
import tempfile
import pandas as pd
import base64
import io
import math
import re
import logging
from datetime import datetime

try:
    import altair as alt
except ImportError:
    alt = None

from datasage import Analyzer
from datasage.cleaner import OutlierDetector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_ROOT = Path('examples') / 'output'
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = OUTPUT_ROOT / 'upload_history.json'
MAX_MB = 500
WARN_MB = 100
ALLOWED_FILE_TYPES = ['csv', 'xls', 'xlsx']
MAX_HISTORY_ENTRIES = 30

st.set_page_config(page_title='DATASAGE - Live Analyzer', layout='wide')
st.title('DATASAGE — Live Analyzer (Upload CSV / Excel)')


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal."""
    # Remove any path components
    filename = Path(filename).name
    # Remove any non-alphanumeric characters except common file chars
    filename = re.sub(r'[^\w\-. ]', '_', filename)
    # Limit length
    return filename[:100]


def load_history():
    if HISTORY_FILE.exists():
        try:
            with HISTORY_FILE.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Failed to load history: %s", e)
            return []
    return []


def save_history(entry: dict):
    try:
        history = load_history()
        history.insert(0, entry)
        history = history[:MAX_HISTORY_ENTRIES]
        with HISTORY_FILE.open('w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.warning("Failed to save history: %s", e)


def format_bytes(size) -> str:
    if size is None:
        return 'Unknown'
    size = float(size)
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:3.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def compute_health_score(missing_cells: int, duplicate_rows: int, anomaly_rows: int, rows: int, columns: int) -> tuple[int, str]:
    total_cells = max(rows * columns, 1)
    missing_ratio = missing_cells / total_cells
    duplicate_ratio = min(duplicate_rows / max(rows, 1), 1.0)
    anomaly_ratio = min(anomaly_rows / max(rows, 1), 1.0)

    score = 100
    score -= min(missing_ratio * 100, 40)
    score -= min(duplicate_ratio * 50, 30)
    score -= min(anomaly_ratio * 50, 30)
    score = max(0, min(int(score), 100))

    if score >= 85:
        label = 'Excellent'
    elif score >= 70:
        label = 'Good'
    elif score >= 50:
        label = 'Needs attention'
    else:
        label = 'Poor'

    return score, label


def inject_theme_css(theme: str):
    if theme == 'dark':
        css = '''
            <style>
            .stApp, .reportview-container, .main {
                background-color: #0b1220 !important;
                color: #e2e8f0 !important;
            }
            .block-container {
                background-color: #0b1220 !important;
                color: #e2e8f0 !important;
            }
            .stButton>button, .stDownloadButton>button {
                background-color: #2563eb !important;
                color: #f8fafc !important;
                border-color: #1d4ed8 !important;
            }
            .stSidebar {
                background-color: #0f172a !important;
                color: #e2e8f0 !important;
            }
            .st-bf {
                background-color: #111827 !important;
            }
            .stMarkdown, .stDataFrame, .stMetric, .stText, .stCaption, .stSubheader, .stHeader {
                color: #e2e8f0 !important;
            }
            .css-1d391kg, .css-1y0tads, .css-1wrcr25 {
                background-color: #111827 !important;
            }
            </style>
        '''
    else:
        # Light theme: use Streamlit's native light theme (readable by default).
        # Only apply minimal, safe overrides so text stays dark and readable.
        css = '''
            <style>
            .stApp, .reportview-container, .main {
                background-color: #ffffff !important;
                color: #0f172a !important;
            }
            .block-container {
                background-color: #ffffff !important;
                color: #0f172a !important;
            }
            .stButton>button, .stDownloadButton>button {
                background-color: #2563eb !important;
                color: #ffffff !important;
                border-color: #1d4ed8 !important;
            }
            .stSidebar {
                background-color: #f1f5f9 !important;
                color: #0f172a !important;
            }
            .stMarkdown, .stDataFrame, .stMetric, .stText, .stCaption, .stSubheader, .stHeader {
                color: #0f172a !important;
            }
            .stDataFrame [data-testid="stDataFrame"] {
                color: #0f172a !important;
            }
            </style>
        '''
    st.markdown(css, unsafe_allow_html=True)


def compute_feature_scores(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include=['number'])
    if numeric.empty:
        return pd.DataFrame()

    variance = numeric.var().fillna(0)
    relative_corr = numeric.corr().abs().sum() - 1
    missing_pct = df.isnull().mean().fillna(0)
    outlier_report, _, _ = detect_outliers(df)
    outlier_count = pd.Series(outlier_report).reindex(numeric.columns, fill_value=0)

    valid = pd.DataFrame({
        'variance': variance,
        'correlation_strength': relative_corr,
        'missing_pct': missing_pct * 100,
        'outlier_count': outlier_count,
    })
    valid['importance'] = (
        valid['variance'].rank(pct=True) * 0.4 +
        valid['correlation_strength'].rank(pct=True) * 0.3 +
        (1 - valid['missing_pct'] / 100).rank(pct=True) * 0.2 +
        (1 - valid['outlier_count'].rank(pct=True)) * 0.1
    ) * 100
    return valid.sort_values('importance', ascending=False)


def render_feature_insights(df: pd.DataFrame):
    st.subheader('Feature Quality & Importance')
    feature_scores = compute_feature_scores(df)
    if feature_scores.empty:
        st.info('Feature importance is available only for numeric datasets.')
        return

    st.write('Features are ranked by variance, correlation impact, missingness, and outlier sensitivity.')
    st.bar_chart(feature_scores['importance'].head(10))

    selected_feature = st.selectbox('Inspect feature', feature_scores.index[:10])
    feature_series = df[selected_feature]

    st.write(f'**{selected_feature}** summary:')
    st.write(feature_scores.loc[selected_feature])

    if pd.api.types.is_numeric_dtype(feature_series):
        st.line_chart(feature_series.dropna().reset_index(drop=True).head(200))
        numeric_data = feature_series.dropna().to_frame(name='value')
        if alt is not None:
            hist = alt.Chart(numeric_data).mark_bar(opacity=0.8, cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
                alt.X('value:Q', bin=alt.Bin(maxbins=20), title='Value'),
                alt.Y('count():Q', title='Frequency'),
                tooltip=[alt.Tooltip('count():Q', title='Count'), alt.Tooltip('value:Q', title='Value', format='.2f')]
            ).properties(height=320, width='container')
            st.altair_chart(hist, use_container_width=True)
        else:
            binned = pd.cut(feature_series.dropna(), bins=10)
            binned_counts = binned.value_counts().sort_index()
            binned_counts.index = binned_counts.index.astype(str)
            st.bar_chart(binned_counts)
    else:
        st.bar_chart(feature_series.fillna('Missing').astype(str).value_counts().head(10))


def render_wellness_dashboard(health_score=None, missing_pct=None, duplicate_pct=None, anomaly_pct=None):
    st.subheader('Dataset Wellness Dashboard')

    def render_health_gauge(score: 'int | None') -> str:
        if score is None:
            return ""
        angle = 180 - (score / 100) * 180
        angle_rad = angle * 3.14159265 / 180
        x = 100 + 90 * math.cos(angle_rad)
        y = 110 - 90 * math.sin(angle_rad)
        large_arc_flag = 1 if score > 50 else 0
        return f"""
        <div style='display:flex;justify-content:center;'>
            <svg viewBox='0 0 200 140' width='280' height='200'>
                <defs>
                    <linearGradient id='g1' x1='0%' y1='0%' x2='100%' y2='0%'>
                        <stop offset='0%' stop-color='#1f77b4'/>
                        <stop offset='100%' stop-color='#2ca02c'/>
                    </linearGradient>
                </defs>
                <path d='M10,110 A90,90 0 1 1 190,110' fill='none' stroke='#eee' stroke-width='16' />
                <path d='M10,110 A90,90 0 {large_arc_flag} 0 {x:.2f},{y:.2f}' fill='none' stroke='url(#g1)' stroke-width='16' stroke-linecap='round' />
                <circle cx='100' cy='110' r='10' fill='#555' />
                <text x='100' y='70' text-anchor='middle' font-size='24' fill='#222'>{score}%</text>
                <text x='100' y='95' text-anchor='middle' font-size='14' fill='#555'>Health Score</text>
            </svg>
        </div>
        """

    if health_score is None:
        cols = st.columns(4)
        cols[0].metric('Health score', '—', 'Upload a dataset to populate wellness gauges')
        cols[1].metric('Missing ratio', '—', 'No data yet')
        cols[2].metric('Duplicate ratio', '—', 'No data yet')
        cols[3].metric('Anomaly ratio', '—', 'No data yet')
        return

    st.components.v1.html(render_health_gauge(health_score), height=220)

    cols = st.columns(4)
    cols[0].metric('Health score', f'{health_score}/100', 'Overall wellness')
    cols[1].metric('Missing ratio', f'{missing_pct:.1f}%')
    cols[2].metric('Duplicate ratio', f'{duplicate_pct:.1f}%')
    cols[3].metric('Anomaly ratio', f'{anomaly_pct:.1f}%')

    progress_cols = st.columns(4)
    progress_cols[0].progress(health_score / 100)
    progress_cols[1].progress(max(0.0, min(1.0, 1 - missing_pct / 100)))
    progress_cols[2].progress(max(0.0, min(1.0, 1 - duplicate_pct / 100)))
    progress_cols[3].progress(max(0.0, min(1.0, 1 - anomaly_pct / 100)))


def render_executive_summary(profile_summary, missing_summary, outlier_report, health_score, health_label):
    st.subheader('Executive Summary')
    st.markdown('A premium view of your dataset health, the top bottlenecks, and recommended next steps.')

    top_missing = missing_summary[missing_summary > 0].head(3)
    most_problematic_column = top_missing.index[0] if not top_missing.empty else 'None'
    top_outlier_column = max(outlier_report, key=outlier_report.get) if outlier_report else 'None'
    top_issue = 'Missing values' if int(profile_summary['missing_columns']) > 0 else 'Anomalies detected' if outlier_report else 'Ready for analysis'

    col1, col2, col3 = st.columns(3)
    col1.metric('Data health', f'{health_score}/100', health_label)
    col2.metric('Top issue', top_issue, f'{most_problematic_column}')
    col3.metric('Numeric columns', profile_summary['numeric_columns'], f"Datetime: {profile_summary['datetime_columns']}")

    with st.expander('Guided recommendations for analysts', expanded=False):
        st.write(f'- **Health status:** {health_label}. Aim for scores above 85 for production-ready analysis.')
        if top_missing.any():
            st.write(f'- **Missing data hotspot:** `{most_problematic_column}` contains {top_missing.iloc[0]:.1f}% missing values.')
        if outlier_report:
            st.write(f'- **Outlier focus:** `{top_outlier_column}` has {outlier_report.get(top_outlier_column, 0)} flagged values.')
        st.write('- Clean the dataset, validate schema suggestions, and rerun the report for the premium dashboard snapshot.')


def render_dashboard_charts(missing_pct, duplicate_pct, anomaly_pct, dtype_counts, outlier_report, missing_summary):
    st.subheader('Wellness Charts')
    st.markdown('Visual summary of dataset health and data quality.')

    metrics_df = pd.DataFrame({
        'metric': ['Missing', 'Duplicates', 'Anomalies'],
        'ratio': [missing_pct, duplicate_pct, anomaly_pct],
    }).set_index('metric')
    st.bar_chart(metrics_df)

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.markdown('**Column Type Distribution**')
        st.bar_chart(dtype_counts)

    with chart_cols[1]:
        if not missing_summary.empty:
            top_missing = missing_summary[missing_summary > 0].head(5)
            st.markdown('**Top missing columns**')
            st.bar_chart(top_missing)
        else:
            st.markdown('**Top missing columns**')
            st.write('No missing values detected.')

    if outlier_report:
        st.markdown('**Outlier counts by column**')
        st.bar_chart(pd.Series(outlier_report, name='outlier_count'))
    else:
        st.markdown('**Outlier counts by column**')
        st.write('No numeric outliers detected.')


def safe_read_data(uploaded_file, filename, sheet_name=None):
    uploaded_file.seek(0)
    extension = Path(filename).suffix.lower()

    if extension == '.xlsx':
        try:
            return pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl'), None
        except Exception as e:
            raise ValueError(f'Failed to parse Excel file: {e}')

    if extension == '.xls':
        try:
            return pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='xlrd'), None
        except Exception as e:
            raise ValueError(f'Failed to parse Excel file: {e}')

    try:
        return pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='warn'), None
    except Exception as e:
        uploaded_file.seek(0)
        try:
            return pd.read_csv(uploaded_file, engine='python', on_bad_lines='warn', encoding='latin1'), str(e)
        except Exception as e2:
            raise ValueError(f'Failed to parse CSV. First error: {e}; fallback error: {e2}')


def is_number_like(value) -> bool:
    try:
        float(value)
        return True
    except Exception:
        return False


def is_date_like(value) -> bool:
    try:
        pd.to_datetime(value, errors='raise')
        return True
    except Exception:
        return False


def infer_schema(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sample_size = min(len(df), 200)
    for col in df.columns:
        series = df[col]
        current_type = str(series.dtype)
        missing_pct = float(series.isna().mean() * 100)
        unique_count = int(series.nunique(dropna=True))

        sample = series.dropna().astype(str).head(sample_size)
        numeric_pct = float(sample.map(is_number_like).mean()) if len(sample) else 0.0
        date_pct = float(sample.map(is_date_like).mean()) if len(sample) else 0.0

        if current_type == 'object':
            if numeric_pct >= 0.8:
                suggest_type = 'numeric'
            elif date_pct >= 0.6:
                suggest_type = 'datetime'
            elif unique_count < max(20, len(series) * 0.05):
                suggest_type = 'category'
            else:
                suggest_type = 'string'
        elif current_type.startswith('int') or current_type.startswith('float'):
            if unique_count < max(20, len(series) * 0.05):
                suggest_type = 'category'
            else:
                suggest_type = 'numeric'
        elif 'datetime' in current_type:
            suggest_type = 'datetime'
        else:
            suggest_type = current_type

        top_values = ', '.join(sample.value_counts().head(3).index.astype(str))
        rows.append({
            'column': col,
            'current_type': current_type,
            'suggested_type': suggest_type,
            'missing_pct': round(missing_pct, 2),
            'unique_count': unique_count,
            'sample_values': top_values,
        })

    return pd.DataFrame(rows)


def coerce_schema(df: pd.DataFrame, schema: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for _, row in schema.iterrows():
        col = row['column']
        target = row['suggested_type']
        if target == 'numeric' and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif target == 'datetime' and col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif target == 'category' and col in df.columns:
            df[col] = df[col].astype('category')
    return df


def detect_outliers(df: pd.DataFrame, method: str = 'iqr'):
    detector = OutlierDetector(method=method)
    report = detector.detect(df)
    indices = sorted(detector.outlier_indices)
    return report, indices, detector.outlier_bounds


def profile_dataframe(df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    dtype_counts = df.dtypes.apply(lambda t: t.name).value_counts().to_frame('count')
    summary = {
        'rows': len(df),
        'columns': df.shape[1],
        'numeric_columns': df.select_dtypes(include='number').shape[1],
        'categorical_columns': df.select_dtypes(include=['object', 'category']).shape[1],
        'datetime_columns': df.select_dtypes(include=['datetime']).shape[1],
        'missing_columns': int(df.isnull().any(axis=0).sum()),
    }
    return summary, dtype_counts


def clean_df(df: pd.DataFrame, drop_cols, mean_cols, median_cols, mode_cols, ffill_cols):
    df = df.copy()
    if drop_cols:
        df = df.drop(columns=drop_cols, errors='ignore')
    if mean_cols:
        numeric = [c for c in mean_cols if c in df.select_dtypes(include='number').columns]
        if numeric:
            df[numeric] = df[numeric].fillna(df[numeric].mean())
    if median_cols:
        numeric = [c for c in median_cols if c in df.select_dtypes(include='number').columns]
        if numeric:
            df[numeric] = df[numeric].fillna(df[numeric].median())
    if mode_cols:
        for col in mode_cols:
            if col in df.columns:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode.iloc[0])
    if ffill_cols:
        df[ffill_cols] = df[ffill_cols].ffill()
    return df


history = load_history()

with st.sidebar:
    st.header('Upload history')
    if history:
        for entry in history[:10]:
            st.markdown(
                f"**{entry['name']}**  "
                f"Uploaded: {entry['uploaded_at']}  "
                f"Size: {entry['size']}  "
                f"Output: `{entry['output_dir']}`"
            )
    else:
        st.info('No previous uploads yet.')

    st.markdown('---')
    st.header('Appearance')
    theme = st.radio('Theme', ['light', 'dark'], index=1)
    inject_theme_css(theme)

    st.markdown('---')
    st.header('Analyst workflow')
    st.markdown(
        '1. Upload a CSV or Excel dataset.  \n'
        '2. Review the data health score and profile suggestions.  \n'
        '3. Apply schema coercion and per-column cleaning.  \n'
        '4. Download the cleaned dataset.  \n'
        '5. Generate visualizations and reports.'
    )

st.markdown("Upload a CSV or Excel file (drag & drop). The app now supports malformed CSV fallback, larger files, Excel input, and column-level cleaning.")

uploaded_file = st.file_uploader('Upload data file', type=ALLOWED_FILE_TYPES, accept_multiple_files=False)

if uploaded_file is None:
    st.info('No file uploaded. You can also run the example to generate sample output or upload your CSV here.')
    render_wellness_dashboard()
else:
    file_name = sanitize_filename(uploaded_file.name)
    extension = Path(file_name).suffix.lower()
    sheet_name = None
    if extension in ['.xls', '.xlsx']:
        try:
            uploaded_file.seek(0)
            excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl' if extension == '.xlsx' else None)
            sheet_name = st.selectbox('Select sheet', excel_file.sheet_names, index=0)
        except Exception as e:
            st.warning(f'Excel sheet preview failed: {e}')

    try:
        df, parse_warning = safe_read_data(uploaded_file, file_name, sheet_name=sheet_name)
    except ValueError as e:
        st.error(str(e))
        df = None
        parse_warning = None

    if parse_warning:
        st.warning('Parsed with warnings: ' + parse_warning)

    if df is not None:
        missing_cells = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())
        st.subheader('Preview of uploaded data')
        st.write(f'Rows: {df.shape[0]}, Columns: {df.shape[1]}')
        st.metric('Missing cells', missing_cells)
        st.metric('Duplicate rows', duplicate_rows)
        st.dataframe(df.head(100))

        missing_columns = int(df.isnull().any(axis=0).sum())
        profile_summary, dtype_counts = profile_dataframe(df)
        outlier_report, anomaly_indices, outlier_bounds = detect_outliers(df)
        anomaly_rows = len(anomaly_indices)

        data_health_score, health_label = compute_health_score(
            missing_cells,
            duplicate_rows,
            anomaly_rows,
            df.shape[0],
            df.shape[1],
        )

        render_wellness_dashboard(
            health_score=data_health_score,
            missing_pct=float(missing_cells / max(df.shape[0] * df.shape[1], 1) * 100),
            duplicate_pct=float(duplicate_rows / max(df.shape[0], 1) * 100),
            anomaly_pct=float(anomaly_rows / max(df.shape[0], 1) * 100),
        )

        if missing_cells > 0:
            missing_summary = (df.isnull().mean() * 100).round(2).sort_values(ascending=False)
            st.write('Top columns with missing data:')
            st.table(missing_summary[missing_summary > 0].head(10))
        else:
            missing_summary = pd.Series(dtype=float)

        render_executive_summary(profile_summary, missing_summary, outlier_report, data_health_score, health_label)

        with st.expander('Column type distribution'):
            st.dataframe(dtype_counts)

        render_dashboard_charts(
            missing_pct=float(missing_cells / max(df.shape[0] * df.shape[1], 1) * 100),
            duplicate_pct=float(duplicate_rows / max(df.shape[0], 1) * 100),
            anomaly_pct=float(anomaly_rows / max(df.shape[0], 1) * 100),
            dtype_counts=dtype_counts,
            outlier_report=outlier_report,
            missing_summary=missing_summary,
        )

        render_feature_insights(df)

        if anomaly_rows > 0:
            st.metric('Potential anomaly rows', anomaly_rows)
            st.write('Potential outliers detected per numeric column:')
            st.table(pd.Series(outlier_report, name='outlier_count').sort_values(ascending=False).to_frame())
            anomaly_preview = df.loc[anomaly_indices].head(50)
            st.write('Preview of rows flagged as potential anomalies:')
            st.dataframe(anomaly_preview)
        else:
            st.metric('Potential anomaly rows', 0)

        with st.expander('Why the health score matters'):
            st.write(
                'The health score is based on missing values, duplicate rows, and detected anomalies. '
                'Use it to quickly understand whether the dataset is ready for analysis or requires additional cleaning.'
            )

        numeric_columns = df.select_dtypes(include='number').columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        all_columns = df.columns.tolist()

        schema_df = infer_schema(df)
        suggested_casts = schema_df[schema_df['suggested_type'].isin(['numeric', 'datetime', 'category'])]

        with st.expander('Data profile & schema suggestions', expanded=True):
            st.write('This profile helps you understand data quality, schema issues, and recommended type conversions.')
            st.write('Use the suggested schema changes to coerce columns before cleaning.')
            st.dataframe(schema_df[['column', 'current_type', 'suggested_type', 'missing_pct', 'unique_count', 'sample_values']].set_index('column'))

            auto_cast = st.checkbox('Auto-coerce suggested column types', value=False)
            if auto_cast:
                df = coerce_schema(df, suggested_casts)
                st.success('Suggested type coercions applied. Review the preview before analysis.')
                numeric_columns = df.select_dtypes(include='number').columns.tolist()
                categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
                all_columns = df.columns.tolist()

        with st.expander('Advanced column-level cleaning options'):
            st.write('Use these options to target cleaning at specific columns before analysis.')
            drop_cols = st.multiselect('Drop columns', options=all_columns)
            mean_cols = st.multiselect('Fill missing with mean', options=numeric_columns)
            median_cols = st.multiselect('Fill missing with median', options=numeric_columns)
            mode_cols = st.multiselect('Fill missing with mode', options=all_columns)
            ffill_cols = st.multiselect('Forward-fill columns', options=all_columns)
            if not mean_cols and not median_cols and not mode_cols and not ffill_cols and not drop_cols:
                st.help('Select columns to apply per-column cleaning before analysis.')

        col1, col2 = st.columns([2, 1])
        with col2:
            st.header('Run options')
            handle_missing = st.selectbox('Default missing strategy', ['drop_column', 'drop_row', 'mean', 'median', 'mode', 'forward_fill'], index=2)
            handle_outliers = st.checkbox('Handle outliers', value=True)
            outlier_strategy = st.selectbox('Outlier strategy', ['cap', 'remove'], index=0)
            remove_duplicates = st.checkbox('Remove duplicates', value=True)
            run_btn = st.button('Run analysis')

        if run_btn:
            try:
                uploaded_file.seek(0, io.SEEK_END)
                fsize = uploaded_file.tell()
                uploaded_file.seek(0)
            except Exception:
                fsize = None

            if fsize and fsize > MAX_MB * 1024 * 1024:
                st.error(f'File is too large ({format_bytes(fsize)}). Limit {MAX_MB} MB.')
            else:
                if fsize and fsize > WARN_MB * 1024 * 1024:
                    st.warning(f'Large file ({format_bytes(fsize)}). Processing may take longer and use more memory.')

                try:
                    cleaned_df = clean_df(df, drop_cols, mean_cols, median_cols, mode_cols, ffill_cols)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    output_dir = OUTPUT_ROOT / f'upload_{timestamp}'
                    output_dir.mkdir(parents=True, exist_ok=True)

                    st.info('Cleaned dataset is ready for download before report generation.')
                    download_name = f"{Path(file_name).stem}_cleaned.csv"
                    cleaned_csv = cleaned_df.to_csv(index=False).encode('utf-8')
                    st.download_button('Download cleaned CSV', data=cleaned_csv, file_name=download_name, mime='text/csv')

                    try:
                        excel_buffer = io.BytesIO()
                        cleaned_df.to_excel(excel_buffer, index=False, engine='openpyxl')
                        excel_bytes = excel_buffer.getvalue()
                        st.download_button(
                            'Download cleaned Excel',
                            data=excel_bytes,
                            file_name=f"{Path(file_name).stem}_cleaned.xlsx",
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        )
                    except Exception as e:
                        logger.warning("Excel export failed: %s", e)
                        st.warning('Excel export is unavailable for this dataset.')

                    analyzer = Analyzer(cleaned_df)

                    prog = st.progress(0)
                    step = 0

                    with st.spinner('Cleaning data...'):
                        analyzer.clean(
                            handle_missing=handle_missing,
                            handle_outliers=handle_outliers,
                            outlier_strategy=outlier_strategy,
                            remove_duplicates=remove_duplicates,
                        )
                        step += 1
                        prog.progress(int(step / 5 * 100))

                    with st.spinner('Analyzing data...'):
                        insights = analyzer.analyze()
                        step += 1
                        prog.progress(int(step / 5 * 100))

                    with st.spinner('Generating visualizations...'):
                        analyzer.visualize(output_dir=str(output_dir))
                        step += 1
                        prog.progress(int(step / 5 * 100))

                    with st.spinner('Generating text report...'):
                        txt_path = output_dir / 'analysis_report.txt'
                        analyzer.generate_report(filepath=str(txt_path), format='text')
                        step += 1
                        prog.progress(int(step / 5 * 100))

                    with st.spinner('Generating PDF report...'):
                        pdf_path = output_dir / 'analysis_report.pdf'
                        analyzer.generate_report(filepath=str(pdf_path), format='pdf', include_charts=True)
                        step += 1
                        prog.progress(100)

                    st.success('Analysis complete — results saved to: ' + str(output_dir))

                    history_entry = {
                        'name': file_name,
                        'uploaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'size': format_bytes(fsize),
                        'output_dir': str(output_dir),
                    }
                    save_history(history_entry)

                    imgs = sorted([p for p in output_dir.iterdir() if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif')], key=lambda p: p.name)
                    if imgs:
                        st.header('Visualizations')
                        for img in imgs:
                            st.image(str(img), caption=img.name, width=700)

                    if txt_path.exists():
                        st.header('Text Report')
                        st.code(txt_path.read_text(encoding='utf-8'))

                    if pdf_path.exists():
                        st.header('PDF Report')
                        try:
                            pdf_bytes = pdf_path.read_bytes()
                            b64 = base64.b64encode(pdf_bytes).decode('utf-8')
                            pdf_display = f'<embed src="data:application/pdf;base64,{b64}" width="100%" height="800" type="application/pdf" />'
                            st.components.v1.html(pdf_display, height=800)
                            st.download_button('Download PDF', data=pdf_bytes, file_name=pdf_path.name, mime='application/pdf')
                        except Exception as e:
                            logger.error("Failed to display PDF: %s", e)
                            st.error(f'Could not display PDF: {e}')

                    st.markdown(f"Download folder: `{output_dir}`")
                except Exception as e:
                    logger.error("Analysis failed: %s", e, exc_info=True)
                    st.error(f'Analysis failed: {str(e)}')

st.markdown('---')
st.caption('This app now preserves upload history and supports column-level cleaning options.')