Un "système à intégrateur unique" (ou "single-integrator system" en anglais) est un modèle mathématique simplifié utilisé en robotique et en théorie de contrôle pour décrire le mouvement d'un robot ou d'un agent autonome. 

### Description
Dans un système à intégrateur unique, la dynamique de l'agent est décrite par une simple intégration de sa vitesse pour obtenir sa position. En d'autres termes, le modèle suppose que l'accélération est négligeable et que la position de l'agent peut être directement obtenue en intégrant sa vitesse.

### Modèle Mathématique
Pour un agent mobile en deux dimensions, le modèle d'un intégrateur unique est donné par les équations suivantes :
\[ \dot{x} = u_x \]
\[ \dot{y} = u_y \]

- \( x \) et \( y \) représentent les coordonnées de position de l'agent.
- \( \dot{x} \) et \( \dot{y} \) sont les dérivées de \( x \) et \( y \) par rapport au temps, c'est-à-dire les composantes de la vitesse de l'agent.
- \( u_x \) et \( u_y \) sont les commandes de contrôle qui représentent les composantes de la vitesse dans les directions \( x \) et \( y \).

### Utilisation
Les systèmes à intégrateur unique sont largement utilisés dans le contrôle des robots mobiles pour des raisons de simplicité. Ils permettent de concevoir et d'analyser des algorithmes de contrôle avec des équations linéaires simples, facilitant ainsi la démonstration des propriétés de stabilité et de convergence.

### Exemple
Supposons que nous voulons déplacer un robot d'une position initiale \((x_0, y_0)\) à une position cible \((x_f, y_f)\) en utilisant un contrôle de type intégrateur unique. Les commandes de contrôle pourraient être définies comme suit pour atteindre cette cible :
\[ u_x = k_p (x_f - x) \]
\[ u_y = k_p (y_f - y) \]

où \( k_p \) est un gain de proportionnalité qui détermine la rapidité du mouvement vers la cible.

### Avantages et Limitations
**Avantages :**
- Simplicité du modèle et des calculs de contrôle.
- Convient pour les simulations et les démonstrations théoriques de concepts de contrôle.

**Limitations :**
- Ne prend pas en compte les contraintes dynamiques réelles, comme les limites d'accélération et les inerties.
- Moins réaliste pour des robots avec des dynamiques plus complexes, tels que les robots avec des modèles unicycle ou bicycle.

Pour des explications plus détaillées, vous pouvez consulter les ressources pédagogiques en ligne et des articles de recherche spécialisés en robotique et en théorie de contrôle, comme ceux disponibles sur [arXiv](https://arxiv.org/) et dans les cours de robotique en ligne.