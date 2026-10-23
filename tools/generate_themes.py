# La plataforma solo carga editorScheme como archivo si termina en .xml.
"""Genera los .theme.json y esquemas .xml de NYX y sus variantes con las mismas claves.

Uso: python tools/generate_themes.py src/main/resources
"""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])


def hx(c):
    return c.lstrip("#").upper()


def mix(a, b, t):
    """Mezcla a hacia b en proporción t."""
    a, b = hx(a), hx(b)
    ra = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    rb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ra, rb))


# Capas exactas de la maqueta de referencia (hex entregados con el diseño):
# stripe/editor #0D0C0D < sidebar y barras #121112 < chat #171517 < pestaña activa #1C1A1C.
GLASS_UI = dict(
    stripe="0D0C0D", chrome="121112", bg="121112", editor="0D0C0D", panel="171517", raised="1C1A1C",
    hover="1C1A1C", selection="1C1A1C", selectionInactive="171517", chip="1C1A1C", border="262326",
    accent="C084FC", onAccent="0D0C0D", text="D6D3D1", textBright="FFFFFF", muted="A8A29E",
    disabled="57534E", thumb="2D2C2D", thumbHover="4A494A", lineNumber="3F3F46",
    error="FB7185", warning="F59E0B", success="34D399")

THEMES = {
    # Maqueta de referencia: lila, lavanda, durazno y ámbar sobre negro cálido.
    "NYX": dict(
        ui=GLASS_UI,
        syntax=dict(keyword="C084FC", function="E9D5FF", functionCall="E9D5FF", ident="D6D3D1",
                    punct="E2E8F0", operator="A78BFA", string="FDBA74", klass="F59E0B", interface="F59E0B",
                    number="FB923C", constant="FB923C", field="94A3B8", tag="E2E8F0", attribute="94A3B8",
                    annotation="A78BFA", escape="FB923C", comment="57534E", doc="6B6560"),
        caret="C084FC", keywordFont=0),
    # Misma sintaxis que favorita sobre negro puro.
    "NYX Blackout": dict(
        ui={**GLASS_UI, "stripe": "000000", "chrome": "0A090A", "bg": "0A090A", "editor": "000000",
            "panel": "100F10", "raised": "161416", "hover": "161416", "selection": "161416",
            "selectionInactive": "100F10", "chip": "161416", "border": "1C1A1C", "thumb": "262426"},
        syntax=dict(keyword="C084FC", function="E9D5FF", functionCall="E9D5FF", ident="D6D3D1",
                    punct="E2E8F0", operator="A78BFA", string="FDBA74", klass="F59E0B", interface="F59E0B",
                    number="FB923C", constant="FB923C", field="94A3B8", tag="E2E8F0", attribute="94A3B8",
                    annotation="A78BFA", escape="FB923C", comment="57534E", doc="6B6560"),
        caret="C084FC", keywordFont=0),
    # Variante gris: casi monocromo, keywords lila, strings grises, línea activa #1E1C1F.
    "NYX Graphite": dict(
        ui={**GLASS_UI, "stripe": "100F10", "chrome": "141314", "bg": "141314", "editor": "0E0D0E",
            "panel": "1A181A", "raised": "1E1C1F", "hover": "1E1C1F", "selection": "1E1C1F",
            "chip": "1E1C1F", "caretRow": "1E1C1F", "lineNumberActive": "C084FC"},
        syntax=dict(keyword="C084FC", function="F5F5F4", functionCall="F5F5F4", ident="F5F5F4",
                    punct="D6D3D1", operator="D6D3D1", string="A8A29E", klass="F5F5F4", interface="F5F5F4",
                    number="F59E0B", constant="F59E0B", field="D6D3D1", tag="F5F5F4", attribute="A1A1AA",
                    annotation="C084FC", escape="F59E0B", comment="52525B", doc="52525B"),
        caret="C084FC", keywordFont=0),
    # Variante azul: keywords lila, funciones azules, strings menta, números ámbar.
    "NYX Eclipse": dict(
        ui=GLASS_UI,
        syntax=dict(keyword="C084FC", function="60A5FA", functionCall="60A5FA", ident="F5F5F4",
                    punct="D6D3D1", operator="C084FC", string="6EE7B7", klass="93C5FD", interface="93C5FD",
                    number="F59E0B", constant="F59E0B", field="D6D3D1", tag="60A5FA", attribute="F5F5F4",
                    annotation="C084FC", escape="F59E0B", comment="57534E", doc="6B6560"),
        caret="C084FC", keywordFont=0),
}

# Clave UI -> rol de la paleta. "*" cubre todo componente sin clave explícita.
UI_KEYS = {
    "*": {
        "background": "bg", "foreground": "text", "infoForeground": "muted",
        "selectionBackground": "selection", "selectionForeground": "textBright",
        "selectionInactiveBackground": "selectionInactive", "selectionBackgroundInactive": "selectionInactive",
        "disabledForeground": "disabled", "inactiveForeground": "muted",
        "borderColor": "border", "separatorColor": "border", "lineSeparatorColor": "border",
        "hoverBackground": "hover", "focusColor": "accent", "focusedBorderColor": "accent",
    },
    "ActionButton.hoverBackground": "hover", "ActionButton.hoverBorderColor": "hover",
    "ActionButton.pressedBackground": "selection", "ActionButton.pressedBorderColor": "selection",
    "Borders.color": "border", "Borders.ContrastBorderColor": "border",
    "Button.background": "raised", "Button.foreground": "text",
    "Button.startBorderColor": "border", "Button.endBorderColor": "border", "Button.focusedBorderColor": "accent",
    "Button.default.startBackground": "accent", "Button.default.endBackground": "accent",
    "Button.default.foreground": "onAccent", "Button.default.startBorderColor": "accent",
    "Button.default.endBorderColor": "accent", "Button.default.focusedBorderColor": "accent",
    "Button.default.focusColor": "accent",
    "ComboBox.background": "panel", "ComboBox.nonEditableBackground": "panel",
    "ComboBox.ArrowButton.background": "panel", "ComboBox.ArrowButton.nonEditableBackground": "panel",
    "ComboBox.selectionBackground": "selection", "ComboBoxButton.background": "panel",
    "CompletionPopup.background": "panel", "CompletionPopup.selectionBackground": "selection",
    "CompletionPopup.selectionInactiveBackground": "selectionInactive", "CompletionPopup.matchForeground": "accent",
    "Component.borderColor": "border", "Component.disabledBorderColor": "border",
    "Component.focusColor": "accent", "Component.focusedBorderColor": "accent",
    "Component.iconColor": "muted", "Component.hoverIconColor": "text",
    "Component.errorFocusColor": "error", "Component.inactiveErrorFocusColor": "error",
    "Component.warningFocusColor": "warning", "Component.inactiveWarningFocusColor": "warning",
    "Counter.background": "accent", "Counter.foreground": "onAccent",
    "DefaultTabs.background": "bg", "DefaultTabs.borderColor": "border", "DefaultTabs.hoverBackground": "hover",
    "DefaultTabs.underlineColor": "accent", "DefaultTabs.inactiveUnderlineColor": "muted",
    "DefaultTabs.underlinedTabBackground": "raised", "DefaultTabs.underlinedTabForeground": "textBright",
    "DragAndDrop.areaBackground": "selection",
    "Editor.background": "editor", "Editor.foreground": "text", "Editor.shortcutForeground": "accent",
    "Editor.SearchField.background": "panel", "Editor.Toolbar.borderColor": "border",
    "EditorPane.background": "editor",
    "EditorTabs.background": "chrome", "EditorTabs.borderColor": "border", "EditorTabs.hoverBackground": "hover",
    "EditorTabs.selectedBackground": "editor", "EditorTabs.inactiveColoredFileBackground": "editor",
    "EditorTabs.underlineColor": "accent", "EditorTabs.inactiveUnderlineColor": "muted",
    "EditorTabs.underlinedTabBackground": "raised", "EditorTabs.underlinedTabForeground": "textBright",
    "GotItTooltip.background": "raised", "GotItTooltip.foreground": "text", "GotItTooltip.borderColor": "border",
    "Group.separatorColor": "border",
    "InplaceRefactoringPopup.background": "panel", "InplaceRefactoringPopup.borderColor": "border",
    "Label.foreground": "text", "Label.disabledForeground": "disabled", "Label.infoForeground": "muted",
    "Link.activeForeground": "accent", "Link.hoverForeground": "accent",
    "Link.pressedForeground": "accent", "Link.visitedForeground": "accent",
    "List.background": "bg", "List.hoverBackground": "hover", "List.selectionBackground": "selection",
    "List.selectionInactiveBackground": "selectionInactive", "List.selectionForeground": "textBright",
    "MainMenu.background": "chrome", "MainMenu.foreground": "text", "MainMenu.selectionBackground": "selection",
    "MainToolbar.background": "chrome", "MainToolbar.inactiveBackground": "chrome", "MainToolbar.foreground": "text",
    "MainToolbar.Dropdown.hoverBackground": "hover", "MainToolbar.Dropdown.pressedBackground": "selection",
    "MainToolbar.Icon.hoverBackground": "hover", "MainToolbar.Icon.pressedBackground": "selection",
    "MainWindow.background": "chrome",
    "Menu.background": "panel", "Menu.foreground": "text", "Menu.borderColor": "border",
    "Menu.separatorColor": "border", "Menu.selectionBackground": "selection",
    "MenuBar.background": "chrome", "MenuBar.borderColor": "border",
    "MenuItem.background": "panel", "MenuItem.selectionBackground": "selection", "MenuItem.acceleratorForeground": "muted",
    "NavBar.borderColor": "border",
    "Notification.background": "panel", "Notification.foreground": "text", "Notification.borderColor": "border",
    "NotificationsToolwindow.newNotification.background": "raised",
    "NotificationsToolwindow.Notification.hoverBackground": "hover",
    "Panel.background": "bg",
    "ParameterInfo.background": "panel", "ParameterInfo.foreground": "text",
    "ParameterInfo.borderColor": "border", "ParameterInfo.currentParameterForeground": "accent",
    "PasswordField.background": "panel",
    "Plugins.background": "bg", "Plugins.SearchField.background": "panel", "Plugins.SectionHeader.background": "bg",
    "Plugins.lightSelectionBackground": "selection", "Plugins.hoverBackground": "hover",
    "Plugins.Tab.selectedBackground": "selection", "Plugins.Tab.hoverBackground": "hover",
    "Popup.background": "panel", "Popup.borderColor": "border", "Popup.inactiveBorderColor": "border",
    "Popup.separatorColor": "border", "Popup.Header.activeBackground": "panel",
    "Popup.Header.inactiveBackground": "panel", "Popup.Advertiser.background": "panel",
    "Popup.Advertiser.foreground": "muted", "Popup.Toolbar.background": "panel", "Popup.Toolbar.borderColor": "border",
    "PopupMenu.background": "panel", "PopupMenu.selectionBackground": "selection",
    "ProgressBar.trackColor": "raised", "ProgressBar.progressColor": "accent",
    "ProgressBar.indeterminateStartColor": "accent", "ProgressBar.indeterminateEndColor": "raised",
    "RunWidget.background": "raised", "RunWidget.foreground": "text",
    "RunWidget.hoverBackground": "hover", "RunWidget.pressedBackground": "selection",
    "ScrollBar.background": "bg", "ScrollBar.trackColor": "bg",
    "ScrollBar.thumbColor": "thumb", "ScrollBar.thumbBorderColor": "thumb",
    "ScrollBar.hoverThumbColor": "thumbHover", "ScrollBar.hoverThumbBorderColor": "thumbHover",
    "ScrollBar.Transparent.thumbColor": "thumb", "ScrollBar.Transparent.thumbBorderColor": "thumb",
    "ScrollBar.Transparent.hoverThumbColor": "thumbHover", "ScrollBar.Transparent.hoverThumbBorderColor": "thumbHover",
    "ScrollBar.Mac.thumbColor": "thumb", "ScrollBar.Mac.thumbBorderColor": "thumb",
    "ScrollBar.Mac.hoverThumbColor": "thumbHover", "ScrollBar.Mac.hoverThumbBorderColor": "thumbHover",
    "ScrollBar.Mac.Transparent.thumbColor": "thumb", "ScrollBar.Mac.Transparent.thumbBorderColor": "thumb",
    "ScrollBar.Mac.Transparent.hoverThumbColor": "thumbHover",
    "ScrollBar.Mac.Transparent.hoverThumbBorderColor": "thumbHover",
    "ScrollPane.background": "bg",
    "SearchEverywhere.Header.background": "panel", "SearchEverywhere.SearchField.background": "panel",
    "SearchEverywhere.SearchField.borderColor": "border", "SearchEverywhere.Tab.selectedBackground": "selection",
    "SearchEverywhere.List.separatorColor": "border", "SearchEverywhere.Advertiser.background": "panel",
    "SearchEverywhere.Advertiser.foreground": "muted",
    "Separator.separatorColor": "border",
    "SidePanel.background": "bg",
    "SpeedSearch.background": "raised", "SpeedSearch.foreground": "text",
    "SpeedSearch.borderColor": "border", "SpeedSearch.errorForeground": "error",
    "StatusBar.background": "chrome", "StatusBar.borderColor": "border", "StatusBar.hoverBackground": "hover",
    "StatusBar.Widget.hoverBackground": "hover", "StatusBar.Widget.pressedBackground": "selection",
    "StatusBar.Breadcrumbs.foreground": "muted", "StatusBar.Breadcrumbs.hoverBackground": "hover",
    "StatusBar.Breadcrumbs.selectionBackground": "selection", "StatusBar.Breadcrumbs.floatingBackground": "panel",
    "TabbedPane.background": "bg", "TabbedPane.contentAreaColor": "bg", "TabbedPane.hoverColor": "hover",
    "TabbedPane.focusColor": "raised", "TabbedPane.underlineColor": "accent", "TabbedPane.disabledUnderlineColor": "muted",
    "Table.background": "bg", "Table.stripeColor": "panel", "Table.gridColor": "border",
    "Table.hoverBackground": "hover", "Table.selectionBackground": "selection",
    "Table.selectionInactiveBackground": "selectionInactive",
    "TableHeader.background": "panel", "TableHeader.bottomSeparatorColor": "border", "TableHeader.separatorColor": "border",
    "TextArea.background": "bg", "TextField.background": "panel", "TextPane.background": "bg",
    "TitlePane.background": "chrome", "TitlePane.inactiveBackground": "chrome", "TitlePane.Button.hoverBackground": "hover",
    "ToggleButton.onBackground": "accent", "ToggleButton.onForeground": "onAccent",
    "ToggleButton.offBackground": "raised", "ToggleButton.buttonColor": "text",
    "Toolbar.Floating.background": "panel",
    "ToolTip.background": "raised", "ToolTip.foreground": "text", "ToolTip.borderColor": "border",
    "ToolTip.infoForeground": "muted", "ToolTip.Actions.background": "panel",
    "ToolWindow.background": "bg",
    "ToolWindow.Header.background": "bg", "ToolWindow.Header.inactiveBackground": "bg",
    "ToolWindow.Header.borderColor": "border", "ToolWindow.HeaderCloseButton.background": "bg",
    "ToolWindow.HeaderTab.hoverBackground": "hover", "ToolWindow.HeaderTab.hoverInactiveBackground": "hover",
    "ToolWindow.HeaderTab.selectedInactiveBackground": "selectionInactive",
    "ToolWindow.HeaderTab.underlineColor": "accent", "ToolWindow.HeaderTab.inactiveUnderlineColor": "muted",
    "ToolWindow.HeaderTab.underlinedTabBackground": "raised", "ToolWindow.HeaderTab.underlinedTabInactiveBackground": "bg",
    "ToolWindow.Button.hoverBackground": "hover", "ToolWindow.Button.selectedBackground": "chip",
    "ToolWindow.Button.selectedForeground": "textBright",
    "ToolWindow.Stripe.background": "stripe", "ToolWindow.Stripe.borderColor": "border",
    "Tree.background": "bg", "Tree.hoverBackground": "hover", "Tree.selectionBackground": "selection",
    "Tree.selectionInactiveBackground": "selectionInactive", "Tree.selectionForeground": "textBright",
    "Tree.modifiedItemForeground": "accent",
    "ValidationTooltip.errorBackground": "panel", "ValidationTooltip.errorBorderColor": "error",
    "ValidationTooltip.warningBackground": "panel", "ValidationTooltip.warningBorderColor": "warning",
    "VersionControl.Log.Commit.currentBranchBackground": "raised", "VersionControl.Log.Commit.hoveredBackground": "hover",
    "Viewport.background": "bg",
    "WelcomeScreen.background": "bg", "WelcomeScreen.Details.background": "bg", "WelcomeScreen.separatorColor": "border",
    "WelcomeScreen.SidePanel.background": "panel", "WelcomeScreen.Projects.background": "bg",
    "WelcomeScreen.Projects.selectionBackground": "selection",
    "WelcomeScreen.Projects.selectionInactiveBackground": "selectionInactive",
}


def ref(role):
    return "nyx" + role[0].upper() + role[1:]


def theme_json(name, t, scheme_file):
    ui = {}
    for key, role in UI_KEYS.items():
        ui[key] = {k: ref(r) for k, r in role.items()} if isinstance(role, dict) else ref(role)
    # Sin máscara para que las pestañas inactivas no se vean grisáceas.
    ui["EditorTabs.inactiveMaskColor"] = "#00000000"
    # Sin rayas de indentación en árboles (Project, dependencias); ClassicPainter las pinta con Tree.hash.
    ui["Tree.paintLines"] = False
    ui["Tree.hash"] = "#00000000"
    ui["SearchMatch.startBackground"] = "#" + t["ui"]["accent"] + "66"
    ui["SearchMatch.endBackground"] = "#" + t["ui"]["accent"] + "66"
    return {
        "name": name,
        "author": "NYX Devs",
        "dark": True,
        "editorScheme": "/" + scheme_file,
        "colors": {ref(k): "#" + v for k, v in t["ui"].items()},
        "ui": ui,
    }


def attr(name, fg=None, bg=None, font=None, effect=None, effect_type=None, stripe=None):
    opts = [("FOREGROUND", fg), ("BACKGROUND", bg), ("FONT_TYPE", font),
            ("EFFECT_COLOR", effect), ("EFFECT_TYPE", effect_type), ("ERROR_STRIPE_COLOR", stripe)]
    body = "".join(f'\n        <option name="{k}" value="{v}" />' for k, v in opts if v is not None)
    return f'    <option name="{name}">\n      <value>{body}\n      </value>\n    </option>'


def icls(name, t):
    u, s = t["ui"], t["syntax"]
    bg = u["editor"]
    text, ident = s["punct"], s["ident"]
    green, red, yellow = u["success"], u["error"], u["warning"]
    strong = t["keywordFont"] or None
    search_bg = mix(u["accent"], bg, 0.70)
    caret_ident = mix(u["accent"], bg, 0.85)
    write_ident = mix(s["annotation"], bg, 0.78)

    colors = {
        "CARET_COLOR": t["caret"], "CARET_ROW_COLOR": u.get("caretRow") or mix(bg, "FFFFFF", 0.035),
        "CONSOLE_BACKGROUND_KEY": bg, "GUTTER_BACKGROUND": bg,
        "LINE_NUMBERS_COLOR": u["lineNumber"],
        "LINE_NUMBER_ON_CARET_ROW_COLOR": u.get("lineNumberActive") or u["text"],
        "INDENT_GUIDE": u["border"], "SELECTED_INDENT_GUIDE": u["thumbHover"], "VISUAL_INDENT_GUIDE": u["border"],
        # La selección de listas (#1C1A1C) es muy sutil para texto; en el editor va teñida de acento.
        "SELECTION_BACKGROUND": mix(u["accent"], bg, 0.78), "SELECTION_FOREGROUND": "",
        "TEARLINE_COLOR": u["border"], "SELECTED_TEARLINE_COLOR": u["muted"],
        "RIGHT_MARGIN_COLOR": u["border"], "METHOD_SEPARATORS_COLOR": u["border"],
        "WHITESPACES": u["thumb"], "SOFT_WRAP_SIGN_COLOR": u["thumb"],
        "FOLDED_TEXT_BORDER_COLOR": u["border"],
        "ADDED_LINES_COLOR": mix(green, bg, 0.35), "MODIFIED_LINES_COLOR": mix(s["klass"], bg, 0.35),
        "DELETED_LINES_COLOR": mix(red, bg, 0.35), "WHITESPACES_MODIFIED_LINES_COLOR": mix(yellow, bg, 0.5),
        "ANNOTATIONS_COLOR": u["muted"], "VCS_ANNOTATIONS_COLOR_1": u["raised"],
        "DOCUMENTATION_COLOR": u["panel"], "LOOKUP_COLOR": u["panel"], "NOTIFICATION_BACKGROUND": u["panel"],
        "INFORMATION_HINT": u["raised"], "QUESTION_HINT": u["raised"], "ERROR_HINT": mix(red, bg, 0.8),
        "FILESTATUS_ADDED": green, "FILESTATUS_MODIFIED": s["klass"], "FILESTATUS_DELETED": u["muted"],
        "FILESTATUS_UNKNOWN": red, "FILESTATUS_IGNORED": u["disabled"],
    }

    a = [
        # Fallbacks de la plataforma: los lenguajes heredan de estos DEFAULT_*.
        attr("TEXT", fg=text, bg=bg),
        attr("DEFAULT_IDENTIFIER", fg=ident),
        attr("DEFAULT_KEYWORD", fg=s["keyword"], font=strong),
        attr("DEFAULT_NUMBER", fg=s["number"]),
        attr("DEFAULT_STRING", fg=s["string"]),
        attr("DEFAULT_VALID_STRING_ESCAPE", fg=s["escape"]),
        attr("DEFAULT_INVALID_STRING_ESCAPE", fg=red, effect=red, effect_type=2),
        attr("DEFAULT_LINE_COMMENT", fg=s["comment"], font=2),
        attr("DEFAULT_BLOCK_COMMENT", fg=s["comment"], font=2),
        attr("DEFAULT_DOC_COMMENT", fg=s["doc"], font=2),
        attr("DEFAULT_DOC_COMMENT_TAG", fg=s["doc"], font=3),
        attr("DEFAULT_DOC_MARKUP", fg=s["doc"]),
        attr("DEFAULT_FUNCTION_DECLARATION", fg=s["function"]),
        attr("DEFAULT_FUNCTION_CALL", fg=s["functionCall"]),
        attr("DEFAULT_INSTANCE_METHOD", fg=s["functionCall"]),
        attr("DEFAULT_STATIC_METHOD", fg=s["functionCall"], font=2),
        attr("DEFAULT_CLASS_NAME", fg=s["klass"], font=strong),
        attr("DEFAULT_CLASS_REFERENCE", fg=s["klass"]),
        attr("DEFAULT_INTERFACE_NAME", fg=s["interface"], font=strong),
        attr("DEFAULT_METADATA", fg=s["annotation"]),
        attr("DEFAULT_PARAMETER", fg=ident),
        attr("DEFAULT_LOCAL_VARIABLE", fg=ident),
        attr("DEFAULT_REASSIGNED_LOCAL_VARIABLE", fg=ident, effect=u["muted"], effect_type=1),
        attr("DEFAULT_INSTANCE_FIELD", fg=s["field"]),
        attr("DEFAULT_STATIC_FIELD", fg=s["field"], font=2),
        attr("DEFAULT_GLOBAL_VARIABLE", fg=s["field"]),
        attr("DEFAULT_CONSTANT", fg=s["constant"], font=2),
        attr("DEFAULT_PREDEFINED_SYMBOL", fg=s["keyword"]),
        attr("DEFAULT_LABEL", fg=s["annotation"]),
        attr("DEFAULT_OPERATION_SIGN", fg=s["operator"]),
        attr("DEFAULT_BRACES", fg=text), attr("DEFAULT_BRACKETS", fg=text), attr("DEFAULT_PARENTHS", fg=text),
        attr("DEFAULT_DOT", fg=text), attr("DEFAULT_COMMA", fg=text), attr("DEFAULT_SEMICOLON", fg=text),
        attr("DEFAULT_TAG", fg=s["tag"]),
        attr("DEFAULT_ATTRIBUTE", fg=s["attribute"]),
        attr("DEFAULT_ENTITY", fg=s["number"]),
        attr("DEFAULT_TEMPLATE_LANGUAGE_COLOR", fg=text, bg=u["panel"]),
        # Java: Darcula define algunas de estas explícitamente, así que se pisan aquí.
        attr("ANNOTATION_NAME_ATTRIBUTES", fg=s["annotation"]),
        attr("ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES", fg=s["attribute"]),
        attr("INSTANCE_FIELD_ATTRIBUTES", fg=s["field"]),
        attr("INSTANCE_FINAL_FIELD_ATTRIBUTES", fg=s["field"]),
        attr("STATIC_FIELD_ATTRIBUTES", fg=s["field"], font=2),
        attr("STATIC_FINAL_FIELD_ATTRIBUTES", fg=s["constant"], font=2),
        attr("JAVA_KEYWORD", fg=s["keyword"], font=strong),
        attr("JAVA_NUMBER", fg=s["number"]),
        attr("JAVA_STRING", fg=s["string"]),
        attr("JAVA_VALID_STRING_ESCAPE", fg=s["escape"]),
        attr("JAVA_LINE_COMMENT", fg=s["comment"], font=2),
        attr("JAVA_BLOCK_COMMENT", fg=s["comment"], font=2),
        attr("JAVA_DOC_COMMENT", fg=s["doc"], font=2),
        attr("JAVA_OPERATION_SIGN", fg=s["operator"]),
        attr("CLASS_NAME_ATTRIBUTES", fg=s["klass"], font=strong),
        attr("INTERFACE_NAME_ATTRIBUTES", fg=s["interface"], font=strong),
        attr("METHOD_DECLARATION_ATTRIBUTES", fg=s["function"]),
        attr("CONSTRUCTOR_DECLARATION_ATTRIBUTES", fg=s["function"]),
        attr("METHOD_CALL_ATTRIBUTES", fg=s["functionCall"]),
        attr("CONSTRUCTOR_CALL_ATTRIBUTES", fg=s["functionCall"]),
        attr("STATIC_METHOD_ATTRIBUTES", fg=s["functionCall"], font=2),
        attr("LOCAL_VARIABLE_ATTRIBUTES", fg=ident),
        attr("PARAMETER_ATTRIBUTES", fg=ident),
        attr("TYPE_PARAMETER_NAME_ATTRIBUTES", fg=s["interface"]),
        attr("ENUM_NAME_ATTRIBUTES", fg=s["klass"], font=strong),
        attr("ABSTRACT_CLASS_NAME_ATTRIBUTES", fg=s["klass"], font=3),
        attr("IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES", fg=s["field"]),
        attr("JAVA_DOC_TAG", fg=s["doc"], font=3),
        # Estado del editor
        attr("IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg=caret_ident, stripe=s["function"]),
        attr("WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES", bg=write_ident, stripe=s["annotation"]),
        attr("SEARCH_RESULT_ATTRIBUTES", bg=search_bg, stripe=u["accent"]),
        attr("WRITE_SEARCH_RESULT_ATTRIBUTES", bg=write_ident, stripe=s["annotation"]),
        attr("TEXT_SEARCH_RESULT_ATTRIBUTES", fg=u["textBright"], bg=search_bg, stripe=u["accent"]),
        attr("MATCHED_BRACE_ATTRIBUTES", fg=u["textBright"], bg=u["selection"], effect=u["accent"], effect_type=1),
        attr("UNMATCHED_BRACE_ATTRIBUTES", bg=mix(red, bg, 0.7)),
        attr("HYPERLINK_ATTRIBUTES", fg=u["accent"], effect=u["accent"], effect_type=1),
        attr("FOLLOWED_HYPERLINK_ATTRIBUTES", fg=u["accent"], effect=u["accent"], effect_type=1),
        attr("CTRL_CLICKABLE", fg=u["accent"], effect=u["accent"], effect_type=1),
        attr("FOLDED_TEXT_ATTRIBUTES", fg=u["muted"], bg=u["raised"]),
        attr("TODO_DEFAULT", fg=bg, bg=s["interface"], font=1),
        attr("ERRORS_ATTRIBUTES", effect=red, effect_type=2, stripe=red),
        attr("WRONG_REFERENCES_ATTRIBUTES", fg=red),
        attr("WARNING_ATTRIBUTES", effect=yellow, effect_type=2, stripe=yellow),
        attr("WARNINGS_ATTRIBUTES", effect=yellow, effect_type=2, stripe=yellow),
        attr("WEAK_WARNING_ATTRIBUTES", effect=u["muted"], effect_type=2),
        attr("INFO_ATTRIBUTES", effect=u["muted"], effect_type=1),
        attr("NOT_USED_ELEMENT_ATTRIBUTES", fg=u["muted"]),
        attr("DEPRECATED_ATTRIBUTES", effect=u["muted"], effect_type=3),
        attr("MARKED_FOR_REMOVAL_ATTRIBUTES", effect=red, effect_type=3),
        attr("BREAKPOINT_ATTRIBUTES", bg=mix(red, bg, 0.8)),
        attr("EXECUTIONPOINT_ATTRIBUTES", bg=mix(s["klass"], bg, 0.75)),
        attr("INLAY_DEFAULT", fg=u["muted"], bg=u["raised"]),
        attr("INLINE_PARAMETER_HINT", fg=u["muted"], bg=u["raised"]),
        attr("INLINE_PARAMETER_HINT_HIGHLIGHTED", fg=u["textBright"], bg=u["selection"]),
        attr("BOOKMARKS_ATTRIBUTES", stripe=u["accent"]),
        attr("BREADCRUMBS_DEFAULT", fg=u["muted"]),
        attr("BREADCRUMBS_HOVERED", fg=u["textBright"], bg=u["hover"]),
        attr("BREADCRUMBS_CURRENT", fg=u["textBright"], bg=u["selection"]),
        attr("BREADCRUMBS_INACTIVE", fg=u["disabled"]),
        # Diff y merge
        attr("DIFF_INSERTED", bg=mix(green, bg, 0.82), stripe=green),
        attr("DIFF_DELETED", bg=mix(red, bg, 0.82), stripe=red),
        attr("DIFF_MODIFIED", bg=mix(s["klass"], bg, 0.82), stripe=s["klass"]),
        attr("DIFF_CONFLICT", bg=mix(yellow, bg, 0.82), stripe=yellow),
        # Consola
        attr("CONSOLE_NORMAL_OUTPUT", fg=text),
        attr("CONSOLE_ERROR_OUTPUT", fg=red),
        attr("CONSOLE_SYSTEM_OUTPUT", fg=u["muted"]),
        attr("CONSOLE_USER_INPUT", fg=green, font=2),
        attr("LOG_ERROR_OUTPUT", fg=red),
        attr("LOG_WARNING_OUTPUT", fg=yellow),
        attr("LOG_INFO_OUTPUT", fg=text),
        attr("LOG_DEBUG_OUTPUT", fg=u["muted"]),
    ]
    ansi = {"BLACK": u["raised"], "RED": red, "GREEN": green, "YELLOW": yellow, "BLUE": s["klass"],
            "MAGENTA": s["keyword"], "CYAN": s["function"], "GRAY": u["muted"],
            "DARKGRAY": u["disabled"], "WHITE": u["textBright"]}
    for color, value in ansi.items():
        a.append(attr(f"CONSOLE_{color}_OUTPUT", fg=value))
    for color in ("RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN"):
        a.append(attr(f"CONSOLE_{color}_BRIGHT_OUTPUT", fg=mix(ansi[color], "FFFFFF", 0.2)))

    color_lines = "\n".join(f'    <option name="{k}" value="{v}" />' for k, v in colors.items())
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<scheme name="{name}" version="142" parent_scheme="Darcula">
  <metaInfo>
    <property name="created">{name} color scheme</property>
    <property name="ide">IntelliJ IDEA</property>
    <property name="originalScheme">{name}</property>
  </metaInfo>
  <option name="LINE_SPACING" value="1.0" />
  <option name="EDITOR_FONT_SIZE" value="13" />
  <option name="EDITOR_FONT_NAME" value="JetBrains Mono" />
  <colors>
{color_lines}
  </colors>
  <attributes>
{chr(10).join(a)}
  </attributes>
</scheme>
"""


for name, t in THEMES.items():
    base = name.replace(" ", "-")
    (OUT / f"{base}.theme.json").write_text(
        json.dumps(theme_json(name, t, f"{base}.xml"), indent=2) + "\n", encoding="utf-8", newline="\n")
    (OUT / f"{base}.xml").write_text(icls(name, t), encoding="utf-8", newline="\n")
    print("ok", base)
