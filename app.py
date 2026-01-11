import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Palettisation - Méthode Matricielle", layout="wide")

# En-tête avec logo et titre
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    st.image("logo_ofppt.png", width=150)

with col2:
    st.markdown("""
    <h1 style='text-align: center; color: #2E86AB; font-weight: bold; margin-top: 20px;'>
    🚚 APPLICATION DE PALETTISATION 3D
    </h1>
    <h3 style='text-align: center; color: #4A4A4A; font-weight: bold;'>
    Méthode Matricielle d'Optimisation Logistique
    </h3>
    <p style='text-align: center; color: #666; font-size: 16px; margin-top: -10px;'>
    <strong>Réalisé par:</strong> ISMAILI ALAOUI MOHAMED - FORMATEUR EN OFPPT
    </p>
    """, unsafe_allow_html=True)

with col3:
    st.image("logo_ofppt.png", width=150)

st.markdown("---")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("⚙️ Paramètres de la palette")
    
    L = st.number_input("Longueur palette L (cm)", value=120, min_value=50, step=10)
    l = st.number_input("Largeur palette l (cm)", value=80, min_value=50, step=10)
    H = st.number_input("Hauteur maximale H (cm)", value=150, min_value=50, step=10)
    P_max = st.number_input("Poids maximal (kg)", value=1000, min_value=100, step=50)
    
    st.markdown("---")
    st.header("📦 Paramètres du colis")
    
    a = st.number_input("Longueur colis a (cm)", value=40, min_value=5, step=5)
    b = st.number_input("Largeur colis b (cm)", value=30, min_value=5, step=5)
    c = st.number_input("Hauteur colis c (cm)", value=25, min_value=5, step=5)
    p = st.number_input("Poids colis p (kg)", value=10.0, min_value=0.1, step=0.5)
    
    st.markdown("---")
    st.header("🔄 Options d'orientation")
    
    mode_orientation = st.radio(
        "Mode de positionnement:",
        ["Toutes les orientations (6)", "Position à plat uniquement (2)"],
        help="Position à plat = utilise uniquement longueur et largeur du colis"
    )

# Fonction pour créer la visualisation 3D
def create_3d_palette(L, l, H, dim_L, dim_l, dim_h, n_L, n_l, n_H):
    """Crée une visualisation 3D de la palette avec les colis"""
    
    fig = go.Figure()
    
    # Couleurs pour différencier les couches
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
    
    # Dessiner la palette (base)
    palette_vertices = [
        [0, 0, 0], [L, 0, 0], [L, l, 0], [0, l, 0],  # Base inférieure
        [0, 0, -5], [L, 0, -5], [L, l, -5], [0, l, -5]  # Base supérieure (épaisseur 5cm)
    ]
    
    # Faces de la palette
    palette_faces = [
        [0, 1, 2, 3], [4, 5, 6, 7],  # Dessus et dessous
        [0, 1, 5, 4], [1, 2, 6, 5],  # Côtés
        [2, 3, 7, 6], [3, 0, 4, 7]
    ]
    
    palette_x = []
    palette_y = []
    palette_z = []
    palette_i = []
    palette_j = []
    palette_k = []
    
    for face in palette_faces:
        palette_i.extend([face[0], face[0]])
        palette_j.extend([face[1], face[2]])
        palette_k.extend([face[2], face[3]])
    
    for vertex in palette_vertices:
        palette_x.append(vertex[0])
        palette_y.append(vertex[1])
        palette_z.append(vertex[2])
    
    fig.add_trace(go.Mesh3d(
        x=palette_x, y=palette_y, z=palette_z,
        i=palette_i, j=palette_j, k=palette_k,
        color='#8B4513',
        opacity=0.3,
        name='Palette',
        showlegend=True
    ))
    
    # Dessiner chaque colis
    for i_L in range(n_L):
        for i_l in range(n_l):
            for i_H in range(n_H):
                # Position du colis
                x_start = i_L * dim_L
                y_start = i_l * dim_l
                z_start = i_H * dim_h
                
                # Couleur selon la couche
                color = colors[i_H % len(colors)]
                
                # Créer un parallélépipède pour chaque colis
                vertices = [
                    [x_start, y_start, z_start],
                    [x_start + dim_L, y_start, z_start],
                    [x_start + dim_L, y_start + dim_l, z_start],
                    [x_start, y_start + dim_l, z_start],
                    [x_start, y_start, z_start + dim_h],
                    [x_start + dim_L, y_start, z_start + dim_h],
                    [x_start + dim_L, y_start + dim_l, z_start + dim_h],
                    [x_start, y_start + dim_l, z_start + dim_h]
                ]
                
                x = [v[0] for v in vertices]
                y = [v[1] for v in vertices]
                z = [v[2] for v in vertices]
                
                # Définir les faces du parallélépipède
                i = [0, 0, 0, 0, 1, 1, 2, 2, 4, 4]
                j = [1, 2, 4, 3, 2, 5, 3, 6, 5, 7]
                k = [2, 3, 5, 4, 6, 6, 7, 7, 6, 6]
                
                fig.add_trace(go.Mesh3d(
                    x=x, y=y, z=z,
                    i=i, j=j, k=k,
                    color=color,
                    opacity=0.7,
                    showlegend=False,
                    hovertemplate=f'<b>Colis</b><br>Position: L={i_L+1}, l={i_l+1}, H={i_H+1}<br>Couche: {i_H+1}<extra></extra>'
                ))
    
    # Mise en page
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Longueur (cm)', range=[0, L * 1.1]),
            yaxis=dict(title='Largeur (cm)', range=[0, l * 1.1]),
            zaxis=dict(title='Hauteur (cm)', range=[-10, H * 1.1]),
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        title=dict(
            text=f'Visualisation 3D - {n_L}×{n_l}×{n_H} = {n_L*n_l*n_H} colis',
            x=0.5,
            xanchor='center'
        ),
        height=600,
        showlegend=True,
        hovermode='closest'
    )
    
    return fig

# Fonction pour calculer les orientations
def calculer_orientations(L, l, H, P_max, a, b, c, p, mode="toutes"):
    if mode == "plat":
        # Position à plat uniquement : on utilise a et b en base, c toujours en hauteur
        orientations = [
            ("a×b×c", a, b, c),  # Orientation 1: longueur selon L
            ("b×a×c", b, a, c),  # Orientation 2: largeur selon L
        ]
    else:
        # Les 6 orientations possibles d'un colis (permutations de a, b, c)
        orientations = [
            ("a×b×c", a, b, c),  # Orientation 1
            ("a×c×b", a, c, b),  # Orientation 2
            ("b×a×c", b, a, c),  # Orientation 3
            ("b×c×a", b, c, a),  # Orientation 4
            ("c×a×b", c, a, b),  # Orientation 5
            ("c×b×a", c, b, a),  # Orientation 6
        ]
    
    resultats = []
    
    for idx, (nom, dim_L, dim_l, dim_h) in enumerate(orientations, 1):
        # Calcul du nombre de colis par dimension
        n_L = int(L // dim_L)  # Nombre selon longueur palette
        n_l = int(l // dim_l)  # Nombre selon largeur palette
        n_H = int(H // dim_h)  # Nombre de couches en hauteur
        
        # Calculs
        nb_colis_couche = n_L * n_l
        nb_couches = n_H
        total_colis = nb_colis_couche * nb_couches
        poids_total = total_colis * p
        
        # Dimensions réelles utilisées
        L_utilisee = n_L * dim_L
        l_utilisee = n_l * dim_l
        H_utilisee = n_H * dim_h
        
        # Taux de remplissage volumétrique
        volume_colis = total_colis * (a * b * c)
        volume_palette = L * l * H
        taux_remplissage = (volume_colis / volume_palette) * 100
        
        # Vérification contrainte de poids
        contrainte_poids = "✓" if poids_total <= P_max else "✗"
        
        resultats.append({
            'N°': idx,
            'Orientation': nom,
            'nL': n_L,
            'nl': n_l,
            'nH': n_H,
            'dim_L': dim_L,
            'dim_l': dim_l,
            'dim_h': dim_h,
            'Combinaison': f"{n_L}×{n_l}×{n_H}",
            'Colis/couche': nb_colis_couche,
            'Couches': nb_couches,
            'Total colis': total_colis,
            'Dimensions (L×l×H)': f"{L_utilisee}×{l_utilisee}×{H_utilisee}",
            'Poids (kg)': round(poids_total, 1),
            'Contrainte P': contrainte_poids,
            'Taux (%)': round(taux_remplissage, 1),
            'Valide': poids_total <= P_max
        })
    
    return resultats

# Bouton de calcul
if st.button("🔍 Calculer la matrice de palettisation", type="primary"):
    with st.spinner("Calcul en cours..."):
        mode = "plat" if "plat" in mode_orientation else "toutes"
        resultats = calculer_orientations(L, l, H, P_max, a, b, c, p, mode)
        df = pd.DataFrame(resultats)
        
        # Filtrer les solutions valides
        df_valides = df[df['Valide'] == True]
        
        # Afficher les statistiques
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Orientations testées", len(df))
        with col2:
            st.metric("Solutions valides", len(df_valides))
        with col3:
            if len(df_valides) > 0:
                st.metric("Max colis", df_valides['Total colis'].max())
            else:
                st.metric("Max colis", 0)
        with col4:
            if len(df_valides) > 0:
                st.metric("Meilleur taux (%)", round(df_valides['Taux (%)'].max(), 1))
            else:
                st.metric("Meilleur taux (%)", 0)
        
        st.markdown("---")
        
        # Affichage de la matrice complète
        if mode == "plat":
            st.subheader("📊 Matrice des 2 orientations à plat")
        else:
            st.subheader("📊 Matrice des 6 orientations possibles")
        
        # Préparer le dataframe pour l'affichage
        df_display = df[['N°', 'Orientation', 'nL', 'nl', 'nH', 'Combinaison', 
                         'Colis/couche', 'Couches', 'Total colis', 
                         'Dimensions (L×l×H)', 'Poids (kg)', 'Contrainte P', 'Taux (%)']].copy()
        
        # Fonction pour colorer les lignes
        def color_rows(row):
            if row['Contrainte P'] == '✗':
                return ['background-color: #ffcccc'] * len(row)
            elif row['Total colis'] == df_valides['Total colis'].max() and len(df_valides) > 0:
                return ['background-color: #ccffcc'] * len(row)
            else:
                return [''] * len(row)
        
        st.dataframe(
            df_display.style.apply(color_rows, axis=1),
            use_container_width=True,
            height=300
        )
        
        st.caption("🟢 Vert = Meilleure solution | 🔴 Rouge = Contrainte de poids non respectée")
        
        # Meilleure solution avec visualisation 3D
        if len(df_valides) > 0:
            st.markdown("---")
            st.subheader("🏆 Meilleure solution")
            meilleure = df_valides.loc[df_valides['Total colis'].idxmax()]
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.success(f"""
                ### Orientation {meilleure['N°']}: {meilleure['Orientation']}
                
                **Combinaison optimale: {meilleure['Combinaison']}**
                
                - {meilleure['nL']} colis en longueur × {meilleure['nl']} colis en largeur × {meilleure['nH']} couches
                - **Total: {meilleure['Total colis']} colis**
                - Poids: {meilleure['Poids (kg)']} kg / {P_max} kg
                - Taux de remplissage: {meilleure['Taux (%)']}%
                - Dimensions utilisées: {meilleure['Dimensions (L×l×H)']} cm
                """)
            
            with col2:
                st.info(f"""
                **Dimensions du colis dans cette orientation:**
                - Longueur sur palette: {meilleure['dim_L']} cm
                - Largeur sur palette: {meilleure['dim_l']} cm
                - Hauteur empilée: {meilleure['dim_h']} cm
                
                **Espaces restants:**
                - Longueur: {L - meilleure['nL'] * meilleure['dim_L']:.1f} cm
                - Largeur: {l - meilleure['nl'] * meilleure['dim_l']:.1f} cm
                - Hauteur: {H - meilleure['nH'] * meilleure['dim_h']:.1f} cm
                """)
            
            # Visualisation 3D de la meilleure solution
            st.markdown("---")
            st.subheader("🎨 Visualisation 3D de la meilleure solution")
            
            fig_3d = create_3d_palette(
                L, l, H,
                meilleure['dim_L'], meilleure['dim_l'], meilleure['dim_h'],
                meilleure['nL'], meilleure['nl'], meilleure['nH']
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)
            
            st.caption("💡 Utilisez la souris pour faire pivoter, zoomer et explorer la palette en 3D. Chaque couleur représente une couche différente.")
            
        else:
            st.error("❌ Aucune solution valide trouvée. Le poids dépasse la capacité maximale pour toutes les orientations.")
        
        # Affichage détaillé de chaque orientation
        st.markdown("---")
        st.subheader("📋 Détail des combinaisons")
        
        for _, row in df.iterrows():
            with st.expander(f"Orientation {row['N°']}: {row['Orientation']} → Combinaison {row['Combinaison']}", 
                           expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Configuration:**
                    - Orientation du colis: **{row['Orientation']}**
                    - Colis en longueur (nL): {row['nL']}
                    - Colis en largeur (nl): {row['nl']}
                    - Couches en hauteur (nH): {row['nH']}
                    - **Combinaison: {row['Combinaison']}**
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Résultats:**
                    - Colis par couche: {row['Colis/couche']}
                    - Nombre de couches: {row['Couches']}
                    - **Total colis: {row['Total colis']}**
                    - Poids total: {row['Poids (kg)']} kg {row['Contrainte P']}
                    - Taux de remplissage: {row['Taux (%)']}%
                    """)
        
        # Export CSV
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger la matrice (CSV)",
            data=csv,
            file_name="matrice_palettisation.csv",
            mime="text/csv"
        )

# Informations sur la méthode
with st.expander("ℹ️ À propos de la méthode matricielle"):
    st.markdown("""
    ### Méthode Matricielle de Palettisation
    
    #### Mode: Toutes les orientations (6)
    Cette méthode calcule les **6 orientations possibles** d'un colis rectangulaire sur une palette:
    
    | N° | Orientation | Description |
    |---|------------|-------------|
    | 1 | a×b×c | Longueur selon L, largeur selon l, hauteur selon H |
    | 2 | a×c×b | Longueur selon L, hauteur selon l, largeur selon H |
    | 3 | b×a×c | Largeur selon L, longueur selon l, hauteur selon H |
    | 4 | b×c×a | Largeur selon L, hauteur selon l, longueur selon H |
    | 5 | c×a×b | Hauteur selon L, longueur selon l, largeur selon H |
    | 6 | c×b×a | Hauteur selon L, largeur selon l, longueur selon H |
    
    #### Mode: Position à plat uniquement (2)
    Cette méthode calcule uniquement les **2 orientations à plat** où la hauteur du colis (c) reste toujours verticale:
    
    | N° | Orientation | Description |
    |---|------------|-------------|
    | 1 | a×b×c | Longueur (a) selon L, largeur (b) selon l, hauteur (c) verticale |
    | 2 | b×a×c | Largeur (b) selon L, longueur (a) selon l, hauteur (c) verticale |
    
    **Pour chaque orientation, on calcule:**
    - nL = ⌊L/dimension_L⌋ (nombre de colis en longueur)
    - nl = ⌊l/dimension_l⌋ (nombre de colis en largeur)
    - nH = ⌊H/dimension_h⌋ (nombre de couches)
    - **Total = nL × nl × nH**
    
    **La combinaison optimale** est celle qui maximise le nombre total de colis tout en respectant la contrainte de poids.
    
    ---
    **Réalisé par:** ISMAILI ALAOUI MOHAMED - FORMATEUR EN OFPPT
    """)