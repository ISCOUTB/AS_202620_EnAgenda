"""Paletas cerradas: nunca se acepta CSS arbitrario desde formularios o cookies."""
TEMAS = {
    "azul": ("Azul clásico · predeterminado", "#12324d", "#e8eef3"),
    "terracota": ("Terracota y arena", "#a55842", "#f0e4d7"),
    "vino": ("Vino y marfil", "#672139", "#f5e6e9"),
    "verde": ("Verde y dorado", "#104c3e", "#e5eee7"),
}

COMUN = {"surface": "#ffffff", "on-accent": "#ffffff"}
PALETAS = {
    "azul": dict(navy="#071c2c", accent="#12324d", **{
        "accent-hover":"#1c4564", "accent-light":"#e8eef3", "champagne":"#b99a88", "champagne-light":"#f1e8e1",
        "background":"#f5f6f8", "text":"#172937", "muted":"#626d76", "border":"#dfe3e7", "focus":"#946a48",
        "sidebar-text":"#f8f3ed", "sidebar-muted":"#c4cdd4", "sidebar-active":"#1a3448",
        "summary-start":"#071c2c", "summary-end":"#163c58", "summary-text":"#f8f3ed",
        "auth-bg":"#051420", "auth-card":"#081d2d", "auth-text":"#f8f3ed", "auth-muted":"#c4cdd4", "auth-input":"#061725"}),
    "terracota": dict(navy="#ebe2d4", accent="#a55842", **{
        "accent-hover":"#8e4937", "accent-light":"#f0e4d7", "champagne":"#a55842", "champagne-light":"#eee4d8",
        "background":"#f7f4ee", "text":"#30271f", "muted":"#70675c", "border":"#dfd5c7", "focus":"#98533f",
        "sidebar-text":"#30271f", "sidebar-muted":"#77685b", "sidebar-active":"#e0d2bf",
        "summary-start":"#ede4d8", "summary-end":"#e1d2be", "summary-text":"#30271f",
        "auth-bg":"#e9dfd1", "auth-card":"#f8f5ef", "auth-text":"#30271f", "auth-muted":"#70675c", "auth-input":"#efe6d9"}),
    "vino": dict(navy="#330d1d", accent="#672139", **{
        "accent-hover":"#802d4d", "accent-light":"#f5e6e9", "champagne":"#c7aa94", "champagne-light":"#f2e3d6",
        "background":"#f6efdf", "text":"#321820", "muted":"#78666a", "border":"#e1d4c6", "focus":"#976b46",
        "sidebar-text":"#f7ebdb", "sidebar-muted":"#dbc3bf", "sidebar-active":"#5d1e33",
        "summary-start":"#4a1329", "summary-end":"#772c46", "summary-text":"#f7ebdb",
        "auth-bg":"#280917", "auth-card":"#330d1d", "auth-text":"#f7ebdb", "auth-muted":"#dbc3bf", "auth-input":"#2c0b19"}),
    "verde": dict(navy="#082f26", accent="#104c3e", **{
        "accent-hover":"#1a604e", "accent-light":"#e5eee7", "champagne":"#b9aa79", "champagne-light":"#eee8d6",
        "background":"#f5f2e8", "text":"#18362b", "muted":"#647267", "border":"#dedbca", "focus":"#86783d",
        "sidebar-text":"#f5f0dc", "sidebar-muted":"#c2d0bc", "sidebar-active":"#17483b",
        "summary-start":"#082f26", "summary-end":"#195847", "summary-text":"#f5f0dc",
        "auth-bg":"#05241c", "auth-card":"#082f26", "auth-text":"#f5f0dc", "auth-muted":"#c2d0bc", "auth-input":"#072a21"}),
}


def normalizar_tema(tema):
    return {"violeta": "azul", "rosa": "vino"}.get(tema, tema) if tema in (*TEMAS, "violeta", "rosa") else "azul"


def variables_tema(tema):
    return {**COMUN, **PALETAS[normalizar_tema(tema)]}
