from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from services.gestion_magasin import (
    rechercher_produit,
    afficher_ventes_console,
    consulter_stock,
    enregistrer_vente_console,
    annuler_vente_console
)
from database.db import initialiser_db

console = Console()

def afficher_menu_principal():
    initialiser_db()

    while True:
        console.print(Panel.fit("[bold cyan]Système de Caisse[/bold cyan]", title="Menu Principal122"))

        console.print("[green]1[/green]. Rechercher un produit")
        console.print("[green]2[/green]. Consulter le stock")
        console.print("[green]3[/green]. Enregistrer une vente")
        console.print("[green]4[/green]. Annuler une vente")
        console.print("[green]5[/green]. Afficher les ventes")
        console.print("[red]0[/red]. Quitter")

        choix = Prompt.ask("\n[bold yellow]Votre choix[/bold yellow]")

        if choix == "1":
            rechercher_produit()
        elif choix == "2":
            consulter_stock()
        elif choix == "3":
            enregistrer_vente_console()
        elif choix == "4":
            annuler_vente_console()
        elif choix == "5":
            afficher_ventes_console()
        elif choix == "0":
            console.print("[bold red]Au revoir ![/bold red]")
            break
        else:
            console.print("[bold red]Choix invalide.[/bold red]")
        console.input("\nAppuyez sur [cyan]Entrée[/cyan] pour continuer...")
