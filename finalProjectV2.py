import flet as ft
import asyncio
import random

def main(page: ft.Page):
    page.title = "Simulador World Soccer Champs"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 420
    page.window.height = 800
    page.padding = 30

    team_home = {"name": "Brasil", "attack": 88, "defense": 82, "score": 0}
    team_away = {"name": "Argentina", "attack": 85, "defense": 80, "score": 0}

    # --- UI Principal ---
    time_text = ft.Text("00'", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_400)
    match_title = ft.Text(f"{team_home['name']} vs {team_away['name']}", size=16, color=ft.Colors.GREY_400)
    score_text = ft.Text("0 - 0", size=50, weight=ft.FontWeight.BOLD)
    events_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # --- Animação do Campinho ---
    home_players = [
        ft.Container(width=8, height=8, bgcolor=ft.Colors.YELLOW, shape=ft.BoxShape.CIRCLE, 
                     animate_position=300, left=random.randint(10, 140), top=random.randint(10, 90)) 
        for _ in range(5)
    ]
    away_players = [
        ft.Container(width=8, height=8, bgcolor=ft.Colors.BLUE, shape=ft.BoxShape.CIRCLE, 
                     animate_position=300, left=random.randint(150, 280), top=random.randint(10, 90)) 
        for _ in range(5)
    ]

    # Borda padrão das linhas do campo
    white_side = ft.BorderSide(2, ft.Colors.WHITE)
    full_border = ft.Border(top=white_side, bottom=white_side, left=white_side, right=white_side)

    pitch = ft.Stack(
        width=300, height=110,
        controls=[
            # Fundo verde com borda
            ft.Container(width=300, height=110, bgcolor=ft.Colors.GREEN_800, border=full_border),
            # Linha de meio de campo
            ft.Container(width=2, height=110, bgcolor=ft.Colors.WHITE, left=150, top=0),
            # Círculo central
            ft.Container(width=30, height=30, border=full_border, border_radius=15, left=135, top=40),
            # Pequenas áreas
            ft.Container(width=30, height=50, border=full_border, left=0, top=30),
            ft.Container(width=30, height=50, border=full_border, left=268, top=30),
        ] + home_players + away_players
    )

    # --- Sistema de Interação Aprimorado ---
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

    # Botões de Primeira Escolha
    btn_chutar = ft.ElevatedButton("Chutar ao Gol", data="chutar", on_click=on_base_click, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
    btn_tocar = ft.ElevatedButton("Trabalhar a Bola", data="tocar", on_click=on_base_click, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
    base_actions_row = ft.Row([btn_chutar, btn_tocar], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    # Botões de Segunda Escolha (Passe)
    btn_cruzar = ft.ElevatedButton("Cruzar na Área", data="cruzar", on_click=on_sub_click, bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE)
    btn_ensaiada = ft.ElevatedButton("Jogada Ensaiada", data="ensaiada", on_click=on_sub_click, bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE)
    pass_actions_row = ft.Row([btn_cruzar, btn_ensaiada], alignment=ft.MainAxisAlignment.CENTER, visible=False)

    # Sub-menu visual: O Gol (Chute)
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
        events_list.controls.append(
            ft.Container(
                content=ft.Text(msg, color=ft.Colors.WHITE, size=14),
                bgcolor=bgcolor, padding=10, border_radius=8,
                alignment=ft.alignment.Alignment.CENTER_LEFT
            )
        )
        events_list.scroll_to(offset=-1, duration=200)

    async def run_match(e):
        start_btn.disabled = True
        team_home["score"] = 0
        team_away["score"] = 0
        score_text.value = "0 - 0"
        events_list.controls.clear()
        page.update()

        for minute in range(1, 94):
            time_text.value = f"{minute}'"
            
            # Movimentação dos jogadores no campinho
            for p in home_players + away_players:
                p.left = random.randint(10, 280)
                p.top = random.randint(10, 90)

            if random.random() < 0.10:
                home_advantage = team_home["attack"] / (team_home["attack"] + team_away["defense"])
                
                # BRASIL ATACA
                if random.random() < home_advantage:
                    for p in home_players: p.left = random.randint(150, 280)
                    
                    log_event(f"⏳ {minute}' - O {team_home['name']} armou o ataque! Qual a sua decisão?", ft.Colors.BLUE_GREY_800)
                    
                    base_actions_row.visible = True
                    page.update()
                    
                    base_action_event.clear()
                    await base_action_event.wait()
                    base_actions_row.visible = False
                    
                    # 1. ESCOLHEU CHUTAR
                    if base_choice == "chutar":
                        log_event(f"👀 Ajeitou o corpo pra bater... Onde você vai colocar a bola?", ft.Colors.CYAN_800)
                        goal_ui.visible = True
                        page.update()
                        
                        sub_action_event.clear()
                        await sub_action_event.wait()
                        goal_ui.visible = False
                        
                        if sub_choice in ["angulo_esq", "angulo_dir"]:
                            if random.random() < 0.35:
                                team_home["score"] += 1
                                log_event(f"⚽ GOLAÇO! No ângulo! A coruja estava lá e foi acordada!", ft.Colors.GREEN_800)
                            else:
                                log_event(f"❌ Pegou muito embaixo e isolou a bola pra arquibancada...", ft.Colors.RED_800)
                        elif sub_choice in ["rast_esq", "rast_dir"]:
                            if random.random() < 0.50:
                                team_home["score"] += 1
                                log_event(f"⚽ GOL! Chute rasteiro de sinuca, no cantinho!", ft.Colors.GREEN_800)
                            else:
                                log_event(f"🧤 O goleiro espalmou o chute rasteiro com a ponta dos dedos!", ft.Colors.ORANGE_800)
                        elif sub_choice == "meio":
                            if random.random() < 0.15:
                                team_home["score"] += 1
                                log_event(f"⚽ GOL! Chutou no meio e o goleirão aceitou! Que frango!", ft.Colors.GREEN_800)
                            else:
                                log_event(f"🧤 Defesa tranquila. Chutou fraco bem no meio do gol.", ft.Colors.RED_800)

                    # 2. ESCOLHEU TOCAR
                    elif base_choice == "tocar":
                        log_event(f"👀 Bola na ponta! Vai cruzar ou tentar a jogada ensaiada?", ft.Colors.CYAN_800)
                        pass_actions_row.visible = True
                        page.update()

                        sub_action_event.clear()
                        await sub_action_event.wait()
                        pass_actions_row.visible = False

                        if sub_choice == "cruzar":
                            if random.random() < 0.45:
                                team_home["score"] += 1
                                log_event(f"⚽ GOL! Cruzamento na medida e o atacante testou firme!", ft.Colors.GREEN_800)
                            else:
                                log_event(f"❌ A zaga subiu mais alto e cortou o cruzamento.", ft.Colors.ORANGE_800)
                        elif sub_choice == "ensaiada":
                            if random.random() < 0.60:
                                team_home["score"] += 1
                                log_event(f"⚽ QUE GOLAÇO! Tabelinha perfeita, defesa desmontada!", ft.Colors.GREEN_800)
                            else:
                                log_event(f"❌ Enfeitaram demais... erraram o passe e cederam o contra-ataque.", ft.Colors.RED_800)
                    
                    score_text.value = f"{team_home['score']} - {team_away['score']}"

                # ARGENTINA ATACA
                else:
                    for p in away_players: p.left = random.randint(10, 150)
                    event_type = random.choices(["goal", "miss"], weights=[0.25, 0.75])[0]
                    
                    if event_type == "goal":
                        team_away["score"] += 1
                        score_text.value = f"{team_home['score']} - {team_away['score']}"
                        log_event(f"⚽ Gol da {team_away['name']}! A zaga dormiu no ponto.", ft.Colors.RED_900)
                    else:
                        log_event(f"🧤 Defesaça do goleiro salva o Brasil do ataque da {team_away['name']}.", ft.Colors.BLUE_800)

            page.update()
            await asyncio.sleep(0.08)

        time_text.value = "FIM"
        log_event("Fim de Jogo! Apita o árbitro.", ft.Colors.PURPLE_800)
        start_btn.disabled = False
        page.update()

    start_btn = ft.ElevatedButton("Iniciar Partida", on_click=run_match, width=200, height=45)

    page.add(
        ft.Row([time_text, ft.Column([match_title, score_text], alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        pitch,
        start_btn,
        base_actions_row, 
        pass_actions_row,
        goal_ui, 
        ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
        events_list
    )

ft.app(target=main)