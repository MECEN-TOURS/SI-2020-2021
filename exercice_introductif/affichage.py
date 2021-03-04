"""Description.

Librairie pour l'affichage demandée à la question 4.
"""
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def affichage_4(reponse_2, reponse_3, x, p):
    x_max, p_max = 0.6, 0.4
    X, P = np.meshgrid(np.linspace(0, x_max), np.linspace(0, p_max))

    D2 = sp.lambdify(args=(x, p), expr=reponse_2["fonction de demande"])(X, P)
    D3 = sp.lambdify(args=(x, p), expr=reponse_3["fonction de demande"])(X, P)

    inter2, = sp.solve(reponse_2["fonction de demande"].subs(p, 0), x)
    inter3, = sp.solve(reponse_3["fonction de demande"].subs(p, 0), x)
    
    figure, repere = plt.subplots()

    repere.spines["left"].set_position("zero")
    repere.spines["bottom"].set_position("zero")
    repere.spines["right"].set_color("none")
    repere.spines["top"].set_color("none")
    repere.set_xlabel("n")
    repere.set_ylabel("p")

    repere.set_xlim(0, x_max)
    repere.set_xticks([0, reponse_2["demande"].evalf(), reponse_3["demande"].evalf()])
    repere.set_xticklabels([0, f"""${sp.latex(reponse_2["demande"])}$""", f"""${sp.latex(reponse_3["demande"])}$"""])
    repere.set_ylim(0, p_max)
    repere.set_yticks([0, reponse_3["prix"].evalf(), reponse_2["prix"].evalf()])
    repere.set_yticklabels([0, f"""${sp.latex(reponse_3["prix"])}$""", f"""${sp.latex(reponse_2["prix"])}$"""])

    repere.plot(
        [0, reponse_3["demande"].evalf()], 
        [reponse_3["prix"].evalf(), reponse_3["prix"].evalf()], 
        color="blue", 
        linestyle="--",
        label="demande partie3"
    )
    repere.plot(
        [reponse_3["demande"].evalf(), reponse_3["demande"].evalf()], 
        [0, reponse_3["prix"].evalf()], 
        color="blue", 
        linestyle="--"
    )

    repere.plot(
        [0, reponse_2["demande"].evalf()], 
        [reponse_2["prix"].evalf(), reponse_2["prix"].evalf()], 
        color="red", 
        linestyle="--",
        label="demande partie2"
    )
    repere.plot(
        [reponse_2["demande"].evalf(), 
         reponse_2["demande"].evalf()], 
        [0, reponse_2["prix"].evalf()], 
        color="red", 
        linestyle="--"
    )

    repere.contour(X, P, D2, levels=[0], colors="blue")
    repere.contour(X, P, D3, levels=[0], colors="red")

    repere.annotate(
        text=f"""$\pi={sp.latex(reponse_2["profit"])}$""", 
        xy=(reponse_2["demande"].evalf(), reponse_2["prix"].evalf()),
        xytext=(1.5 * reponse_2["demande"].evalf(), 1.5 * reponse_2["prix"].evalf()),
        arrowprops=dict(facecolor='red', shrink=0.05),
        color="red",
        fontsize="large"
    )
    repere.annotate(
        text=f"""$\pi={sp.latex(reponse_3["profit"])}$""", 
        xy=(reponse_3["demande"].evalf(), reponse_3["prix"].evalf()),
        xytext=(1.5 * reponse_3["demande"].evalf(), 1.5 * reponse_3["prix"].evalf()),
        arrowprops=dict(facecolor='blue', shrink=0.05),
        color="blue",
        fontsize="large"
    )

    ordonne32, = sp.solve(reponse_3["fonction de demande"].subs(x, inter2), p)
    abc = [reponse_2["demande"].evalf(), inter2.evalf(), inter3.evalf()]
    bas = [reponse_2["prix"].evalf(), 0, 0]
    haut = [reponse_2["prix"].evalf(), ordonne32.evalf(),0]
    repere.fill_between(
        [float(nbr) for nbr in abc],
        [float(nbr) for nbr in bas],
        [float(nbr) for nbr in haut],
        color="blue",
        alpha=0.5
    )

    repere.annotate(
        text="Direct Network Effect",
        xy=(0.33, 0.05),
        xytext=(0.5, 0.1),
        arrowprops=dict(facecolor='black', shrink=0.05),
        fontsize="large"
    )

    repere.legend()
    return figure

def gere_valeur(valeur, expression, p1, p2, P1, P2):
    '''Auxiliaire pour la question 7.'''
    resultat = dict()
    resultat["grille"] = sp.lambdify(args=(p1, p2), expr=(expression - valeur))(P1, P2)
    resultat["p1"], = sp.solve((expression - valeur).subs(p2, 0), p1)
    resultat["p2"], = sp.solve((expression - valeur).subs(p1, 0), p2)
    return resultat

def affichage_7(reponse, p1, p2, n2s):
    p1_max, p2_max = 0.6, 0.6
    P1, P2 = np.meshgrid(np.linspace(0, p1_max, 100), np.linspace(0, p2_max, 100))

    donnees = {
        val: gere_valeur(
            valeur=val, 
            expression=reponse["fonction demande groupe2"], 
            p1=p1, 
            p2=p2, 
            P1=P1, 
            P2=P2
        )
        for val in n2s
    }

    figure, repere = plt.subplots()

    repere.spines["left"].set_position("zero")
    repere.spines["bottom"].set_position("zero")
    repere.spines["right"].set_color("none")
    repere.spines["top"].set_color("none")
    repere.set_xlabel("$p_1$")
    repere.set_ylabel("$p_2$")
    repere.axis("equal")

    repere.set_xlim(0, p1_max)
    repere.set_xticks([donnee["p1"].evalf() for donnee in donnees.values()])
    repere.set_xticklabels([f'${sp.latex(donnee["p1"])}$' for donnee in donnees.values()])
    repere.set_ylim(0, p2_max)
    repere.set_yticks([donnee["p2"].evalf() for donnee in donnees.values()])
    repere.set_yticklabels([f'${sp.latex(donnee["p2"])}$' for donnee in donnees.values()])

    for val, donnee in donnees.items():
        repere.contour(P1, P2, donnee["grille"], levels=[0], colors="blue")
        repere.annotate(
            text=f"$n_2={sp.latex(val)}$",
            xy=(donnee["p1"] / 2, donnee["p2"] / 2),
            xytext=(0.02 +  donnee["p1"] / 2, 0.02 + donnee["p2"] / 2),
            fontsize="large",
            arrowprops=dict(facecolor='black', arrowstyle="->"),
        )

    x_m, y_m = float(max(repere.get_xticks())), float(max(repere.get_yticks()))
    repere.fill_between([0, x_m], [0, 0], [y_m, 0], color="blue", alpha=0.5)

    repere.set_title("Variation de $p_2$ en fonction de $p_1$ à $n_2$ donné")
    return figure