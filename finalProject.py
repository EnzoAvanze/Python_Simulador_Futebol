import flet as ft
import asyncio
import random

def main(page: ft.Page):
    page.title = "Simulador World Soccer Champs"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    team_home = {"name": "Brasil", "attack": 88, "defense": 82, "score": 0}
    team_away = {"name": "Argentina", "attack": 85, "defense": 80, "score": 0}

    time_text = ft.Text("00'", size=55, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_400)
    match_title = ft.Text(f"{team_home['name']} vs {team_away['name']}", size=18, color=ft.Colors.GREY_400)
    score_text = ft.Text("0 - 0", size=60, weight=ft.FontWeight.BOLD)
    events_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # --- NOVO: Sistema de Interação do Jogador ---
    player_choice = None
    action_event = asyncio.Event()

    def on_action_click(e):
        nonlocal player_choice
        player_choice = e.control.data  # Pega se foi 'chutar' ou 'tocar'
        action_event.set()  # Destrava a simulação

    btn_chutar = ft.ElevatedButton("Chutar ao Gol", data="chutar", on_click=on_action_click, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE, visible=False)
    btn_tocar = ft.ElevatedButton("Tocar a Bola", data="tocar", on_click=on_action_click, bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE, visible=False)
    actions_row = ft.Row([btn_chutar, btn_tocar], alignment=ft.MainAxisAlignment.CENTER)

    def log_event(msg, bgcolor):
        events_list.controls.append(
            ft.Container(
                content=ft.Text(msg, color=ft.Colors.WHITE, size=15),
                bgcolor=bgcolor,
                padding=15,
                border_radius=8,
                alignment=ft.alignment.Alignment.CENTER_LEFT
            )
        )

    async def run_match(e):
        start_btn.disabled = True
        team_home["score"] = 0
        team_away["score"] = 0
        score_text.value = "0 - 0"
        events_list.controls.clear()
        page.update()

        for minute in range(1, 94):
            time_text.value = f"{minute}'"
            
            # 10% de chance de algo acontecer a cada minuto
            if random.random() < 0.10:
                home_advantage = team_home["attack"] / (team_home["attack"] + team_away["defense"])
                
                # Brasil (Você) ataca
                if random.random() < home_advantage:
                    log_event(f"⏳ {minute}' - O {team_home['name']} está no ataque! O que você faz?", ft.Colors.BLUE_GREY_800)
                    
                    # Mostra os botões e pausa o relógio
                    btn_chutar.visible = True
                    btn_tocar.visible = True
                    page.update()
                    
                    action_event.clear()
                    await action_event.wait() # A simulação congela aqui esperando seu clique
                    
                    # Esconde os botões após a escolha
                    btn_chutar.visible = False
                    btn_tocar.visible = False
                    
                    # Lógica da escolha
                    if player_choice == "chutar":
                        if random.random() < 0.40: # 40% de chance de gol direto
                            team_home["score"] += 1
                            log_event(f"⚽ GOOOOL! Chute no ângulo do {team_home['name']}!", ft.Colors.GREEN_800)
                        else:
                            log_event(f"🧤 O goleiro da {team_away['name']} defendeu o chute!", ft.Colors.RED_800)
                            
                    elif player_choice == "tocar":
                        if random.random() < 0.70: # 70% de chance de acerto no passe, gerando uma chance mais fácil
                            if random.random() < 0.80: # 80% de chance de gol após passe
                                team_home["score"] += 1
                                log_event(f"⚽ GOOOOL! Jogada trabalhada, gol fácil do {team_home['name']}!", ft.Colors.GREEN_800)
                            else:
                                log_event(f"❌ O atacante do {team_home['name']} furou na hora do chute!", ft.Colors.ORANGE_800)
                        else:
                            log_event(f"❌ Passe interceptado pela zaga da {team_away['name']}.", ft.Colors.RED_800)
                    
                    score_text.value = f"{team_home['score']} - {team_away['score']}"

                # Argentina (Máquina) ataca
                else:
                    event_type = random.choices(["goal", "miss"], weights=[0.25, 0.75])[0]
                    if event_type == "goal":
                        team_away["score"] += 1
                        score_text.value = f"{team_home['score']} - {team_away['score']}"
                        log_event(f"⚽ Gol da {team_away['name']}! Falha na marcação.", ft.Colors.RED_900)
                    else:
                        log_event(f"🧤 Defesa do Brasil salva ataque da {team_away['name']}.", ft.Colors.BLUE_800)

            page.update()
            await asyncio.sleep(0.06)

        time_text.value = "FIM"
        log_event("Fim de Jogo!", ft.Colors.PURPLE_800)
        start_btn.disabled = False
        page.update()

    start_btn = ft.ElevatedButton("Iniciar Partida", on_click=run_match, width=200, height=50)

    page.add(
        time_text,
        match_title,
        score_text,
        start_btn,
        actions_row, # A linha com os botões (escondidos no início)
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        events_list
    )

ft.app(target=main)