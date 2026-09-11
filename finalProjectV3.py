import flet as ft
import asyncio
import random

# Tabela de cores disponíveis para os uniformes
COLOR_MAP = {
    "Amarelo": ft.Colors.YELLOW,
    "Azul": ft.Colors.BLUE_400,
    "Vermelho": ft.Colors.RED_500,
    "Verde": ft.Colors.GREEN_500,
    "Branco": ft.Colors.WHITE,
    "Preto": ft.Colors.GREY_900,
    "Roxo": ft.Colors.PURPLE_400,
    "Laranja": ft.Colors.ORANGE_500,
}

# Times Predefinidos
PRESET_TEAMS = {
    "Brasil": {"attack": 88, "defense": 82, "color": "Amarelo"},
    "Argentina": {"attack": 85, "defense": 80, "color": "Azul"},
    "França": {"attack": 89, "defense": 84, "color": "Azul"},
    "Espanha": {"attack": 86, "defense": 81, "color": "Vermelho"},
    "Alemanha": {"attack": 84, "defense": 83, "color": "Branco"},
    "Personalizado": {"attack": 80, "defense": 80, "color": "Verde"},
}

def main(page: ft.Page):
    page.title = "Simulador World Soccer Champs"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 420
    page.window.height = 800
    page.padding = 25

    # Dados dos Times
    team_home = {"name": "Brasil", "attack": 88, "defense": 82, "color": "Amarelo", "score": 0}
    team_away = {"name": "Argentina", "attack": 85, "defense": 80, "color": "Azul", "score": 0}

    # ==========================================
    # --- UI DO MENU INICIAL (SELEÇÃO) ---
    # ==========================================

    home_shirt_preview = ft.Container(
        width=45, height=45,
        bgcolor=COLOR_MAP[team_home["color"]],
        border_radius=8,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.WHITE24),
            bottom=ft.BorderSide(1, ft.Colors.WHITE24),
            left=ft.BorderSide(1, ft.Colors.WHITE24),
            right=ft.BorderSide(1, ft.Colors.WHITE24),
        ),
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Icon(ft.Icons.CHECKROOM, color=ft.Colors.BLACK if team_home["color"] in ["Amarelo", "Branco"] else ft.Colors.WHITE, size=28)
    )

    away_shirt_preview = ft.Container(
        width=45, height=45,
        bgcolor=COLOR_MAP[team_away["color"]],
        border_radius=8,
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.WHITE24),
            bottom=ft.BorderSide(1, ft.Colors.WHITE24),
            left=ft.BorderSide(1, ft.Colors.WHITE24),
            right=ft.BorderSide(1, ft.Colors.WHITE24),
        ),
        alignment=ft.alignment.Alignment(0, 0),
        content=ft.Icon(ft.Icons.CHECKROOM, color=ft.Colors.BLACK if team_away["color"] in ["Amarelo", "Branco"] else ft.Colors.WHITE, size=28)
    )

    home_preset_dd = ft.Dropdown(
        label="Selecione um Preset",
        options=[ft.dropdown.Option(k) for k in PRESET_TEAMS.keys()],
        value="Brasil",
        width=240,
    )
    home_name_tf = ft.TextField(label="Nome do Seu Time", value="Brasil", width=240)
    home_color_dd = ft.Dropdown(
        label="Cor do Uniforme",
        options=[ft.dropdown.Option(c) for c in COLOR_MAP.keys()],
        value="Amarelo",
        width=180,
    )

    away_preset_dd = ft.Dropdown(
        label="Selecione um Preset",
        options=[ft.dropdown.Option(k) for k in PRESET_TEAMS.keys()],
        value="Argentina",
        width=240,
    )
    away_name_tf = ft.TextField(label="Nome do Adversário", value="Argentina", width=240)
    away_color_dd = ft.Dropdown(
        label="Cor do Uniforme",
        options=[ft.dropdown.Option(c) for c in COLOR_MAP.keys()],
        value="Azul",
        width=180,
    )

    def on_home_preset_change(e):
        preset = PRESET_TEAMS[home_preset_dd.value]
        if home_preset_dd.value != "Personalizado":
            home_name_tf.value = home_preset_dd.value
        home_color_dd.value = preset["color"]
        update_shirt_preview(home_shirt_preview, home_color_dd.value)
        page.update()

    def on_away_preset_change(e):
        preset = PRESET_TEAMS[away_preset_dd.value]
        if away_preset_dd.value != "Personalizado":
            away_name_tf.value = away_preset_dd.value
        away_color_dd.value = preset["color"]
        update_shirt_preview(away_shirt_preview, away_color_dd.value)
        page.update()

    def update_shirt_preview(container, color_name):
        bg = COLOR_MAP[color_name]
        container.bgcolor = bg
        icon_color = ft.Colors.BLACK if color_name in ["Amarelo", "Branco"] else ft.Colors.WHITE
        container.content.color = icon_color

    def on_home_color_change(e):
        update_shirt_preview(home_shirt_preview, home_color_dd.value)
        page.update()

    def on_away_color_change(e):
        update_shirt_preview(away_shirt_preview, away_color_dd.value)
        page.update()

    home_preset_dd.on_change = on_home_preset_change
    away_preset_dd.on_change = on_away_preset_change
    home_color_dd.on_change = on_home_color_change
    away_color_dd.on_change = on_away_color_change

    def start_game(e):
        team_home["name"] = home_name_tf.value or "Casa"
        team_home["color"] = home_color_dd.value
        team_home["attack"] = PRESET_TEAMS.get(home_preset_dd.value, {"attack": 80})["attack"]

        team_away["name"] = away_name_tf.value or "Visitante"
        team_away["color"] = away_color_dd.value
        team_away["attack"] = PRESET_TEAMS.get(away_preset_dd.value, {"attack": 80})["attack"]

        for p in home_players:
            p.bgcolor = COLOR_MAP[team_home["color"]]
        for p in away_players:
            p.bgcolor = COLOR_MAP[team_away["color"]]

        match_title.value = f"{team_home['name']} vs {team_away['name']}"
        score_text.value = "0 - 0"
        time_text.value = "00'"
        events_list.controls.clear()

        # Botão de voltar fica oculto durante a partida
        back_menu_btn.visible = False

        menu_container.visible = False
        match_container.visible = True
        page.update()

    menu_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Text("🏆 Configuração da Partida", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_400),
            
            ft.Container(
                padding=15, bgcolor=ft.Colors.GREY_900, border_radius=12,
                content=ft.Column([
                    ft.Text("🏠 Seu Time (Casa)", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.GREEN_400),
                    home_preset_dd,
                    home_name_tf,
                    ft.Row([home_color_dd, home_shirt_preview], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=10)
            ),

            ft.Container(
                padding=15, bgcolor=ft.Colors.GREY_900, border_radius=12,
                content=ft.Column([
                    ft.Text("✈️ Adversário (Fora)", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_400),
                    away_preset_dd,
                    away_name_tf,
                    ft.Row([away_color_dd, away_shirt_preview], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=10)
            ),

            ft.ElevatedButton(
                "⚽ Ir Para o Jogo",
                on_click=start_game,
                style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE, padding=15),
                width=280
            )
        ]
    )

    # ==========================================
    # --- UI DA PARTIDA (CAMPO & SIMULAÇÃO) ---
    # ==========================================

    time_text = ft.Text("00'", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_400)
    match_title = ft.Text(f"{team_home['name']} vs {team_away['name']}", size=15, color=ft.Colors.GREY_400)
    score_text = ft.Text("0 - 0", size=45, weight=ft.FontWeight.BOLD)
    
    events_list = ft.ListView(
        expand=True,
        spacing=8
    )

    home_players = [
        ft.Container(width=8, height=8, bgcolor=COLOR_MAP[team_home["color"]], shape=ft.BoxShape.CIRCLE, 
                     animate_position=300, left=random.randint(10, 140), top=random.randint(10, 90)) 
        for _ in range(5)
    ]
    away_players = [
        ft.Container(width=8, height=8, bgcolor=COLOR_MAP[team_away["color"]], shape=ft.BoxShape.CIRCLE, 
                     animate_position=300, left=random.randint(150, 280), top=random.randint(10, 90)) 
        for _ in range(5)
    ]

    white_side = ft.BorderSide(2, ft.Colors.WHITE)
    full_border = ft.Border(top=white_side, bottom=white_side, left=white_side, right=white_side)

    pitch = ft.Stack(
        width=300, height=110,
        controls=[
            ft.Container(width=300, height=110, bgcolor=ft.Colors.GREEN_800, border=full_border),
            ft.Container(width=2, height=110, bgcolor=ft.Colors.WHITE, left=150, top=0),
            ft.Container(width=30, height=30, border=full_border, border_radius=15, left=135, top=40),
            ft.Container(width=30, height=50, border=full_border, left=0, top=30),
            ft.Container(width=30, height=50, border=full_border, left=268, top=30),
        ] + home_players + away_players
    )

    base_action_event = asyncio.Event()
    sub_action_event = asyncio.Event()
    base_choice = None
    sub_choice = None

    def on_base_click(e):
        nonlocal base_choice
        base_choice = e.control.data
        base_action_event.set()

    def on_sub_click(e):
        nonlocal sub_choice
        sub_choice = e.control.data
        sub_action_event.set()

    btn_chutar = ft.ElevatedButton("Chutar ao Gol", data="chutar", on_click=on_base_click, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
    btn_tocar = ft.ElevatedButton("Trabalhar a Bola", data="tocar", on_click=on_base_click, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
    base_actions_row = ft.Row([btn_chutar, btn_tocar], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    btn_cruzar = ft.ElevatedButton("Cruzar na Área", data="cruzar", on_click=on_sub_click, bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE)
    btn_ensaiada = ft.ElevatedButton("Jogada Ensaiada", data="ensaiada", on_click=on_sub_click, bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
    pass_actions_row = ft.Row([btn_cruzar, btn_ensaiada], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    goal_border_side = ft.BorderSide(6, ft.Colors.WHITE)
    goal_ui = ft.Container(
        width=250, height=120,
        bgcolor=ft.Colors.GREEN_900,
        border=ft.Border(top=goal_border_side, left=goal_border_side, right=goal_border_side),
        padding=10,
        visible=False,
        content=ft.Column([
            ft.Row([
                ft.ElevatedButton("↖️ Ang", data="angulo_esq", on_click=on_sub_click, width=70, style=ft.ButtonStyle(padding=0)),
                ft.Container(width=30),
                ft.ElevatedButton("↗️ Ang", data="angulo_dir", on_click=on_sub_click, width=70, style=ft.ButtonStyle(padding=0))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.ElevatedButton("↙️ Baixo", data="rast_esq", on_click=on_sub_click, width=70, style=ft.ButtonStyle(padding=0)),
                ft.ElevatedButton("🎯 Meio", data="meio", on_click=on_sub_click, width=70, style=ft.ButtonStyle(padding=0)),
                ft.ElevatedButton("↘️ Baixo", data="rast_dir", on_click=on_sub_click, width=70, style=ft.ButtonStyle(padding=0))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    def log_event(msg, bgcolor):
        # Insere a nova mensagem na PRIMEIRA posição (posição 0).
        # Assim a última ação fica sempre visível no topo da lista.
        events_list.controls.insert(
            0,
            ft.Container(
                content=ft.Text(msg, color=ft.Colors.WHITE, size=14),
                bgcolor=bgcolor, padding=10, border_radius=8,
                alignment=ft.alignment.Alignment(-1, 0)
            )
        )
        page.update()

    async def run_match(e):
        start_btn.disabled = True
        back_menu_btn.visible = False  # Esconde o botão de voltar ao iniciar a partida
        team_home["score"] = 0
        team_away["score"] = 0
        score_text.value = "0 - 0"
        events_list.controls.clear()
        page.update()

        for minute in range(1, 94):
            time_text.value = f"{minute}'"
            
            for p in home_players + away_players:
                p.left = random.randint(10, 280)
                p.top = random.randint(10, 90)

            if random.random() < 0.10:
                home_advantage = team_home["attack"] / (team_home["attack"] + team_away["defense"])
                
                # SEU TIME ATACA
                if random.random() < home_advantage:
                    for p in home_players: p.left = random.randint(150, 280)
                    
                    log_event(f"⏳ {minute}' - O {team_home['name']} armou o ataque! Qual a sua decisão?", ft.Colors.BLUE_GREY_800)
                    
                    base_actions_row.visible = True
                    page.update()
                    
                    base_action_event.clear()
                    await base_action_event.wait()
                    base_actions_row.visible = False
                    
                    if base_choice == "chutar":
                        log_event("👀 Ajeitou o corpo pra bater... Onde você vai colocar a bola?", ft.Colors.CYAN_800)
                        goal_ui.visible = True
                        page.update()
                        
                        sub_action_event.clear()
                        await sub_action_event.wait()
                        goal_ui.visible = False
                        
                        if sub_choice in ["angulo_esq", "angulo_dir"]:
                            if random.random() < 0.35:
                                team_home["score"] += 1
                                log_event("⚽ GOLAÇO! No ângulo! A coruja foi acordada!", ft.Colors.GREEN_800)
                            else:
                                log_event("❌ Pegou muito embaixo e isolou a bola pra arquibancada...", ft.Colors.RED_800)
                        elif sub_choice in ["rast_esq", "rast_dir"]:
                            if random.random() < 0.50:
                                team_home["score"] += 1
                                log_event("⚽ GOL! Chute rasteiro de sinuca, no cantinho!", ft.Colors.GREEN_800)
                            else:
                                log_event("🧤 O goleiro espalmou o chute rasteiro!", ft.Colors.ORANGE_800)
                        elif sub_choice == "meio":
                            if random.random() < 0.15:
                                team_home["score"] += 1
                                log_event("⚽ GOL! Chutou no meio e o goleirão aceitou! Que frango!", ft.Colors.GREEN_800)
                            else:
                                log_event("🧤 Defesa tranquila. Chutou fraco bem no meio.", ft.Colors.RED_800)

                    elif base_choice == "tocar":
                        log_event("👀 Bola na ponta! Vai cruzar ou tentar a jogada ensaiada?", ft.Colors.CYAN_800)
                        pass_actions_row.visible = True
                        page.update()

                        sub_action_event.clear()
                        await sub_action_event.wait()
                        pass_actions_row.visible = False

                        if sub_choice == "cruzar":
                            if random.random() < 0.45:
                                team_home["score"] += 1
                                log_event("⚽ GOL! Cruzamento na medida e o atacante testou firme!", ft.Colors.GREEN_800)
                            else:
                                log_event("❌ A zaga subiu mais alto e cortou o cruzamento.", ft.Colors.ORANGE_800)
                        elif sub_choice == "ensaiada":
                            if random.random() < 0.60:
                                team_home["score"] += 1
                                log_event("⚽ QUE GOLAÇO! Tabelinha perfeita, defesa desmontada!", ft.Colors.GREEN_800)
                            else:
                                log_event("❌ Enfeitaram demais... erraram o passe.", ft.Colors.RED_800)
                    
                    score_text.value = f"{team_home['score']} - {team_away['score']}"

                # ADVERSÁRIO ATACA
                else:
                    for p in away_players: p.left = random.randint(10, 150)
                    event_type = random.choices(["goal", "miss"], weights=[0.25, 0.75])[0]
                    
                    if event_type == "goal":
                        team_away["score"] += 1
                        score_text.value = f"{team_home['score']} - {team_away['score']}"
                        log_event(f"⚽ Gol do {team_away['name']}! A zaga dormiu no ponto.", ft.Colors.RED_900)
                    else:
                        log_event(f"🧤 Defesaça do goleiro salva o {team_home['name']}.", ft.Colors.BLUE_800)

            page.update()
            await asyncio.sleep(0.08)

        time_text.value = "FIM"
        log_event("🏁 Fim de Jogo! Apita o árbitro.", ft.Colors.PURPLE_800)
        
        # Libera o botão de jogar e torna o botão de voltar visível novamente ao término
        start_btn.disabled = False
        back_menu_btn.visible = True
        page.update()

    def go_back_to_menu(e):
        match_container.visible = False
        menu_container.visible = True
        page.update()

    start_btn = ft.ElevatedButton("Iniciar Partida", on_click=run_match, width=160, height=40)
    back_menu_btn = ft.ElevatedButton("◀️ Menu", on_click=go_back_to_menu, width=110, height=40, bgcolor=ft.Colors.GREY_800, visible=False)

    match_container = ft.Column(
        visible=False,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Row([time_text, ft.Column([match_title, score_text], alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            pitch,
            ft.Row([start_btn, back_menu_btn], alignment=ft.MainAxisAlignment.CENTER),
            base_actions_row, 
            pass_actions_row,
            goal_ui, 
            ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
            events_list
        ]
    )

    page.add(menu_container, match_container)

ft.app(target=main)