# styles/voltagent_styles.py
# Centralized Voltagent Design System — QSS tokens + factory functions
# ponytail: single source of truth for all UI styling. Change a color here → changes everywhere.
#
# Vibe: Ethereal High-Tech Dark (#101010 canvas, #1a1a1a panels, #00d992 electric accent)
# Layout: Asymmetrical Panel Grid with Double-Bezel nested container architecture
# Motion: QVariantAnimation color fades (150ms) + QGraphicsDropShadowEffect depth (prepared here, animated in panels)

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QFont


# ─── Layout Macro-Whitespace Tokens ───────────────────────────────────────────
# These are Python ints for use with setContentsMargins() and setSpacing().
# Every panel in the application MUST reference these to maintain spatial rhythm.

MARGIN = 24          # layout.setContentsMargins(24, 24, 24, 24)
SPACING = 16         # layout.setSpacing(16)
MARGIN_COMPACT = 12  # for tightly nested sub-panels
SPACING_COMPACT = 8  # for tightly nested sub-panels
PADDING_BUTTON_H = 10  # vertical button padding
PADDING_BUTTON_W = 16  # horizontal button padding


# ─── Design Tokens ───────────────────────────────────────────────────────────

class Color:
    """Voltagent color palette — dark canvas only, single green accent."""
    # Primary accent
    PRIMARY = "#00d992"
    PRIMARY_SOFT = "#2fd6a1"
    PRIMARY_DEEP = "#10b981"
    ON_PRIMARY = "#101010"

    # Text hierarchy
    INK = "#f2f2f2"
    INK_STRONG = "#ffffff"
    BODY = "#bdbdbd"
    MUTE = "#8b949e"

    # Borders & structure
    HAIRLINE = "#3d3a39"
    HAIRLINE_SOFT = "#b8b3b0"
    HAIRLINE_FOCUS = "#00d992"

    # Surfaces
    CANVAS = "#101010"
    CANVAS_SOFT = "#1a1a1a"
    CANVAS_MID = "#242424"
    CANVAS_TEXT_SOFT = "#f5f6f7"

    # Semantic
    ERROR = "#ef4444"
    WARNING = "#f59e0b"
    SUCCESS = "#10b981"


class Spacing:
    """4px-base spacing scale for QSS string interpolation."""
    XXS = "2px"
    XS = "4px"
    SM = "8px"
    MD = "12px"
    LG = "16px"
    XL = "20px"
    XXL = "24px"
    XXXL = "32px"
    XXXXL = "40px"
    XXXXXL = "48px"


class Rounded:
    """Border-radius scale."""
    NONE = "0px"
    XS = "4px"
    SM = "6px"
    MD = "8px"
    LG = "12px"
    PILL = "9999px"
    FULL = "9999px"


class Typography:
    """Font families and sizes — Inter system font first, SF Mono for code."""
    SANS = "Inter, 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif"
    MONO = "SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    SIZE_XS = "12px"
    SIZE_SM = "14px"
    SIZE_MD = "16px"
    SIZE_LG = "18px"
    SIZE_XL = "24px"
    SIZE_XXL = "32px"

    @staticmethod
    def font_sans(size: int = 14, weight: int = 400) -> QFont:
        return QFont("Segoe UI", size, weight)

    @staticmethod
    def font_mono(size: int = 13, weight: int = 400) -> QFont:
        return QFont("Consolas", size, weight)


# ─── QSS Factory Functions ───────────────────────────────────────────────────
# Each function returns a complete QSS string. All interactive elements define
# :hover and :pressed pseudo-states. Color transitions are prepared here;
# QVariantAnimation-based fades will be wired in the panel classes.

def qss_button_primary() -> str:
    """Electric-green CTA button — pill-shaped, generous padding, full hover/pressed chain."""
    return f"""
        QPushButton {{
            font-weight: 600;
            font-size: 10pt;
            letter-spacing: 0.5px;
            border: none;
            border-radius: {Rounded.SM};
            background-color: {Color.PRIMARY};
            color: {Color.ON_PRIMARY};
            padding: {PADDING_BUTTON_H}px {PADDING_BUTTON_W}px;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: {Color.PRIMARY_SOFT};
        }}
        QPushButton:pressed {{
            background-color: {Color.PRIMARY_DEEP};
            padding-top: {PADDING_BUTTON_H + 1}px;
            padding-bottom: {PADDING_BUTTON_H - 1}px;
        }}
        QPushButton:disabled {{
            background-color: {Color.CANVAS_MID};
            color: {Color.MUTE};
        }}
    """


def qss_button_secondary() -> str:
    """Hairline-on-dark secondary button — canvas background, subtle border, full hover/pressed."""
    return f"""
        QPushButton {{
            font-weight: 600;
            font-size: 9pt;
            letter-spacing: 0.3px;
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.SM};
            background-color: transparent;
            color: {Color.INK};
            padding: {PADDING_BUTTON_H}px {PADDING_BUTTON_W}px;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK_STRONG};
            border: 1px solid {Color.BODY};
        }}
        QPushButton:pressed {{
            background-color: {Color.CANVAS_MID};
            border: 1px solid {Color.HAIRLINE_SOFT};
            padding-top: {PADDING_BUTTON_H + 1}px;
            padding-bottom: {PADDING_BUTTON_H - 1}px;
        }}
        QPushButton:disabled {{
            border-color: {Color.CANVAS_MID};
            color: {Color.MUTE};
        }}
    """


def qss_button_ghost_green() -> str:
    """Text-only green label button — no border, full hover/pressed chain."""
    return f"""
        QPushButton {{
            font-weight: 800;
            font-size: 10pt;
            letter-spacing: 0.5px;
            border: none;
            border-radius: {Rounded.SM};
            background-color: transparent;
            color: {Color.PRIMARY_SOFT};
            padding: {PADDING_BUTTON_H}px {PADDING_BUTTON_W}px;
        }}
        QPushButton:hover {{
            color: {Color.PRIMARY};
            background-color: rgba(0, 217, 146, 0.08);
        }}
        QPushButton:pressed {{
            color: {Color.PRIMARY_DEEP};
            background-color: rgba(0, 217, 146, 0.12);
        }}
        QPushButton:disabled {{
            color: {Color.MUTE};
        }}
    """


def qss_button_danger() -> str:
    """Destructive action button — red accent, full hover/pressed chain."""
    return f"""
        QPushButton {{
            font-weight: 600;
            font-size: 10pt;
            letter-spacing: 0.5px;
            border: none;
            border-radius: {Rounded.SM};
            background-color: {Color.ERROR};
            color: {Color.INK_STRONG};
            padding: {PADDING_BUTTON_H}px {PADDING_BUTTON_W}px;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: #dc2626;
        }}
        QPushButton:pressed {{
            background-color: #b91c1c;
            padding-top: {PADDING_BUTTON_H + 1}px;
            padding-bottom: {PADDING_BUTTON_H - 1}px;
        }}
    """


def qss_input_frame() -> str:
    """Standard text input on dark — hairline border, focus glow, generous padding."""
    return f"""
        QLineEdit {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            padding: 8px 12px;
            min-height: 24px;
            font-size: 11pt;
            font-weight: 500;
            selection-background-color: {Color.PRIMARY};
            selection-color: {Color.ON_PRIMARY};
        }}
        QLineEdit:hover {{
            border: 1px solid {Color.BODY};
        }}
        QLineEdit:focus {{
            border: 1px solid {Color.PRIMARY};
        }}
        QLineEdit:disabled {{
            background-color: {Color.CANVAS};
            color: {Color.MUTE};
            border-color: {Color.CANVAS_MID};
        }}
    """


def qss_text_edit() -> str:
    """Multi-line text edit — matching input frame aesthetic."""
    return f"""
        QTextEdit, QPlainTextEdit {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            padding: 8px 12px;
            font-size: 11pt;
            font-weight: 500;
            selection-background-color: {Color.PRIMARY};
            selection-color: {Color.ON_PRIMARY};
        }}
        QTextEdit:hover, QPlainTextEdit:hover {{
            border: 1px solid {Color.BODY};
        }}
        QTextEdit:focus, QPlainTextEdit:focus {{
            border: 1px solid {Color.PRIMARY};
        }}
    """


def qss_combo_box() -> str:
    """Dropdown combo box — matches input frame, full hover/pressed chain."""
    return f"""
        QComboBox {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            padding: 8px 12px;
            min-height: 24px;
            font-size: 11pt;
            font-weight: 500;
        }}
        QComboBox:hover {{
            border: 1px solid {Color.BODY};
        }}
        QComboBox:focus, QComboBox:on {{
            border: 1px solid {Color.PRIMARY};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            border: none;
            border-left: 1px solid {Color.HAIRLINE};
            border-top-right-radius: {Rounded.XS};
            border-bottom-right-radius: {Rounded.XS};
        }}
        QComboBox::down-arrow {{
            image: none;
            width: 0px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            selection-background-color: {Color.CANVAS_MID};
            selection-color: {Color.PRIMARY};
            padding: 4px;
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 6px 10px;
            border-radius: {Rounded.XS};
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: {Color.CANVAS_MID};
            color: {Color.INK_STRONG};
        }}
    """


def qss_container_panel() -> str:
    """Base container panel — hairline border on canvas, the outer shell of the Double-Bezel."""
    return f"""
        QFrame#containerPanel {{
            background-color: {Color.CANVAS};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.LG};
        }}
    """


def qss_container_inner() -> str:
    """Inner core of the Double-Bezel — sits inside the tray with a softer background."""
    return f"""
        QFrame#containerInner {{
            background-color: {Color.CANVAS_SOFT};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
        }}
    """


def qss_card_feature() -> str:
    """Default feature card — hairline border on canvas, hover elevation prep."""
    return f"""
        QFrame {{
            background-color: {Color.CANVAS};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
        }}
        QFrame:hover {{
            border: 1px solid {Color.BODY};
        }}
        QLabel {{
            color: {Color.INK};
            border: none;
            background: transparent;
        }}
    """


def qss_list_widget() -> str:
    """QListWidget styled as Voltagent feature card — full hover/selected chain."""
    return f"""
        QListWidget {{
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.SM};
            background-color: {Color.CANVAS};
            color: {Color.BODY};
            font-size: 10pt;
            font-weight: 500;
            padding: 4px;
            outline: none;
        }}
        QListWidget::item {{
            padding: 10px 14px;
            border-radius: {Rounded.XS};
            margin-bottom: 4px;
        }}
        QListWidget::item:hover {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK};
        }}
        QListWidget::item:selected {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.PRIMARY};
            font-weight: bold;
        }}
        QListWidget:focus {{
            border: 1px solid {Color.HAIRLINE};
        }}
    """


def qss_panel_input_overlay() -> str:
    """Input overlay panel sitting on top of canvas — complete panel QSS with scrollbar."""
    return f"""
        QFrame#PanelNoi {{
            background-color: {Color.CANVAS_SOFT};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
        }}
        QLabel {{
            color: {Color.INK};
            font-size: 10pt;
            font-weight: 600;
            border: none;
            background: transparent;
        }}
        QLineEdit {{
            background-color: {Color.CANVAS};
            color: {Color.INK};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            padding: 8px 12px;
            min-height: 24px;
            font-size: 11pt;
            font-weight: 500;
        }}
        QLineEdit:hover {{
            border: 1px solid {Color.BODY};
        }}
        QLineEdit:focus {{
            border: 1px solid {Color.PRIMARY};
        }}
        QScrollArea {{
            background: transparent;
            border: none;
        }}
        {qss_scrollbar_vertical(Color.CANVAS_SOFT, Color.HAIRLINE)}
    """


def qss_sidebar() -> str:
    """Right sidebar panel — canvas background, hairline border."""
    return f"""
        QFrame#sidebar {{
            background-color: {Color.CANVAS};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
        }}
        QLabel {{
            color: {Color.INK};
            border: none;
            background: transparent;
        }}
    """


def qss_label_eyebrow() -> str:
    """Uppercase tracked eyebrow label — electric green, wide letter-spacing."""
    return f"""
        QLabel {{
            font-weight: 600;
            font-size: 12pt;
            color: {Color.PRIMARY};
            letter-spacing: 2.52px;
            background: transparent;
            border: none;
        }}
    """


def qss_label_title() -> str:
    """Section title label — white ink, medium weight."""
    return f"""
        QLabel {{
            font-weight: 600;
            font-size: 14px;
            color: {Color.INK};
            letter-spacing: 0.5px;
            background: transparent;
            border: none;
        }}
    """


def qss_label_body() -> str:
    """Body text label — muted body color for secondary content."""
    return f"""
        QLabel {{
            font-weight: 400;
            font-size: 11pt;
            color: {Color.BODY};
            background: transparent;
            border: none;
            line-height: 1.5;
        }}
    """


def qss_divider() -> str:
    """Hairline horizontal divider — 1px line with generous margin."""
    return f"""
        QFrame#divider {{
            color: {Color.HAIRLINE};
            background-color: {Color.HAIRLINE};
            max-height: 1px;
            border: none;
            margin: 8px 0px;
        }}
    """


def qss_scrollbar_vertical(track_color: str = "", handle_color: str = "") -> str:
    """Parameterized vertical scrollbar — thin, rounded, hover highlight on handle."""
    t = track_color or Color.CANVAS
    h = handle_color or Color.HAIRLINE
    return f"""
        QScrollBar:vertical {{
            background: {t};
            width: 8px;
            border-radius: 4px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {h};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {Color.BODY};
        }}
        QScrollBar::handle:vertical:pressed {{
            background: {Color.INK};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
    """


def qss_scrollbar_horizontal(track_color: str = "", handle_color: str = "") -> str:
    """Parameterized horizontal scrollbar — matches vertical aesthetic."""
    t = track_color or Color.CANVAS
    h = handle_color or Color.HAIRLINE
    return f"""
        QScrollBar:horizontal {{
            background: {t};
            height: 8px;
            border-radius: 4px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {h};
            border-radius: 4px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {Color.BODY};
        }}
        QScrollBar::handle:horizontal:pressed {{
            background: {Color.INK};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            border: none;
            background: none;
            width: 0px;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: none;
        }}
    """


def qss_exercise_list_panel() -> str:
    """Complete stylesheet for ExerciseListPanel (menu chính) — full hover/pressed chain on buttons."""
    return f"""
        #ExerciseListPanel {{
            background-color: {Color.CANVAS};
        }}
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}
        #scrollAreaWidgetContents {{
            background-color: transparent;
        }}
        {qss_scrollbar_vertical()}
        QPushButton {{
            background-color: {Color.CANVAS};
            color: {Color.INK};
            font-family: 'Segoe UI', sans-serif;
            font-size: 15pt;
            font-weight: 600;
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.SM};
            padding: 15px 20px;
            margin-bottom: 12px;
            text-align: left;
        }}
        QPushButton:hover {{
            color: {Color.PRIMARY};
            background-color: {Color.CANVAS_SOFT};
            border: 1px solid {Color.PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {Color.CANVAS_MID};
            border: 1px solid {Color.PRIMARY_DEEP};
            padding-top: 16px;
            padding-bottom: 14px;
        }}
        #lbl_author {{
            font-family: 'Segoe UI', sans-serif;
            font-size: 10pt;
            font-weight: 400;
            color: {Color.MUTE};
            letter-spacing: 0.5px;
            background: transparent;
            border: none;
        }}
        #lbl_author:hover {{
            color: {Color.INK};
        }}
    """


def qss_analysis_overlay() -> str:
    """Complete stylesheet for AnalysisOverlayPanel — soft panel, scrollable text."""
    return f"""
        QWidget#AnalysisOverlayPanel {{
            background-color: {Color.CANVAS_SOFT};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
        }}
        QTextBrowser {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.BODY};
            font-family: 'Segoe UI', sans-serif;
            font-size: 11pt;
            padding: 12px 18px;
            border: none;
            selection-background-color: {Color.PRIMARY};
            selection-color: {Color.ON_PRIMARY};
        }}
        {qss_scrollbar_vertical(Color.CANVAS_SOFT, Color.HAIRLINE)}
    """


def qss_canvas() -> str:
    """GraphicArea canvas stylesheet — soft background, hairline border."""
    return f"""
        QWidget#graphicCanvas {{
            background-color: {Color.CANVAS_SOFT};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
        }}
    """


def qss_analysis_title() -> str:
    """Title label inside analysis overlay — electric green, bold."""
    return f"""
        QLabel {{
            color: {Color.PRIMARY};
            font-weight: 900;
            font-size: 14pt;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 0.5px;
            background-color: transparent;
            padding: 4px 0px;
            border: none;
        }}
    """


def qss_analysis_close_button() -> str:
    """Close button inside analysis overlay — matches secondary button aesthetic."""
    return f"""
        QPushButton {{
            background-color: {Color.CANVAS};
            color: {Color.INK};
            font-weight: bold;
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.SM};
            font-family: 'Segoe UI', sans-serif;
            font-size: 10pt;
            padding: 6px 14px;
            min-height: 18px;
        }}
        QPushButton:hover {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.PRIMARY};
            border: 1px solid {Color.PRIMARY};
        }}
        QPushButton:pressed {{
            background-color: {Color.CANVAS_MID};
            border: 1px solid {Color.PRIMARY_DEEP};
            padding-top: 7px;
            padding-bottom: 5px;
        }}
    """


def qss_tab_widget() -> str:
    """QTabWidget styled for dark canvas — hairline tabs, green active indicator."""
    return f"""
        QTabWidget::pane {{
            background-color: {Color.CANVAS};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.MD};
            top: -1px;
        }}
        QTabBar::tab {{
            background-color: {Color.CANVAS};
            color: {Color.MUTE};
            border: 1px solid {Color.HAIRLINE};
            border-bottom: none;
            border-top-left-radius: {Rounded.SM};
            border-top-right-radius: {Rounded.SM};
            padding: 8px 16px;
            font-size: 10pt;
            font-weight: 500;
            margin-right: 2px;
        }}
        QTabBar::tab:hover {{
            background-color: {Color.CANVAS_SOFT};
            color: {Color.INK};
        }}
        QTabBar::tab:selected {{
            background-color: {Color.CANVAS};
            color: {Color.PRIMARY};
            font-weight: 600;
            border-bottom: 2px solid {Color.PRIMARY};
        }}
    """


def qss_progress_bar() -> str:
    """Indeterminate/determinate progress bar — green fill on dark track."""
    return f"""
        QProgressBar {{
            background-color: {Color.CANVAS_SOFT};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            text-align: center;
            font-size: 9pt;
            color: {Color.INK};
            min-height: 8px;
            max-height: 8px;
        }}
        QProgressBar::chunk {{
            background-color: {Color.PRIMARY};
            border-radius: {Rounded.XS};
        }}
    """


def qss_tooltip() -> str:
    """Tooltip — dark floating label with subtle shadow (shadow applied in panel code)."""
    return f"""
        QToolTip {{
            background-color: {Color.CANVAS_MID};
            color: {Color.INK};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            padding: 6px 10px;
            font-size: 10pt;
            font-weight: 500;
        }}
    """


def qss_checkbox() -> str:
    """Checkbox — custom dark styling with green check."""
    return f"""
        QCheckBox {{
            color: {Color.INK};
            font-size: 10pt;
            font-weight: 500;
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            background-color: {Color.CANVAS_SOFT};
        }}
        QCheckBox::indicator:hover {{
            border: 1px solid {Color.BODY};
        }}
        QCheckBox::indicator:checked {{
            background-color: {Color.PRIMARY};
            border: 1px solid {Color.PRIMARY};
        }}
        QCheckBox::indicator:disabled {{
            background-color: {Color.CANVAS};
            border-color: {Color.CANVAS_MID};
        }}
    """


def qss_radio_button() -> str:
    """Radio button — custom dark styling with green dot."""
    return f"""
        QRadioButton {{
            color: {Color.INK};
            font-size: 10pt;
            font-weight: 500;
            spacing: 8px;
        }}
        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.PILL};
            background-color: {Color.CANVAS_SOFT};
        }}
        QRadioButton::indicator:hover {{
            border: 1px solid {Color.BODY};
        }}
        QRadioButton::indicator:checked {{
            background-color: {Color.PRIMARY};
            border: 1px solid {Color.PRIMARY};
        }}
    """


def qss_slider() -> str:
    """Horizontal slider — green handle on dark track."""
    return f"""
        QSlider::groove:horizontal {{
            background: {Color.CANVAS_SOFT};
            border: 1px solid {Color.HAIRLINE};
            border-radius: {Rounded.XS};
            height: 6px;
        }}
        QSlider::handle:horizontal {{
            background: {Color.PRIMARY};
            border: none;
            border-radius: {Rounded.PILL};
            width: 16px;
            height: 16px;
            margin: -6px 0;
        }}
        QSlider::handle:horizontal:hover {{
            background: {Color.PRIMARY_SOFT};
        }}
        QSlider::handle:horizontal:pressed {{
            background: {Color.PRIMARY_DEEP};
        }}
        QSlider::sub-page:horizontal {{
            background: {Color.PRIMARY};
            border-radius: {Rounded.XS};
        }}
    """


# ─── Convenience ─────────────────────────────────────────────────────────────

def apply_qss(widget: QWidget, qss_func, *args, **kwargs):
    """Apply a QSS factory function to a widget."""
    widget.setStyleSheet(qss_func(*args, **kwargs))