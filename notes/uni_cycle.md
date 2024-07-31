Un "modèle unicycle" est une simplification mathématique utilisée en robotique pour décrire le mouvement de robots mobiles qui se déplacent comme un tricycle ou un vélo. Ce modèle est appelé ainsi parce que le robot a une seule roue directrice, ce qui le rend similaire à un monocycle en termes de dynamique de mouvement.

### Description du Modèle
Le modèle unicycle est utilisé pour des robots qui ont une direction de mouvement et une orientation séparées. En d'autres termes, le robot ne peut pas se déplacer latéralement sans changer d'orientation. Il a une vitesse linéaire dans la direction où il est orienté et une vitesse angulaire autour de son centre.

### Modèle Mathématique
Les équations de mouvement pour un modèle unicycle en deux dimensions sont les suivantes :
$\dot{x} = v \cos(\theta)$
$\dot{y} = v \sin(\theta)$
$\dot{\theta} = \omega$

- $(x, y)$ sont les coordonnées de position du robot.
- $\theta$ est l'angle d'orientation du robot par rapport à l'axe $x$.
- $v$ est la vitesse linéaire du robot (tangente à son orientation).
- $\omega$ est la vitesse angulaire (vitesse de rotation).

### Utilisation
Le modèle unicycle est utilisé dans la conception et l'analyse de systèmes de contrôle pour les robots mobiles. Il permet de modéliser et de contrôler des robots de manière à ce qu'ils suivent des trajectoires spécifiques ou atteignent des positions cibles en évitant des obstacles.

### Exemple de Contrôle
Pour déplacer un robot unicycle vers une cible $(x_f, y_f)$, les commandes de contrôle pourraient être définies de la manière suivante :
$v = k_v \sqrt{(x_f - x)^2 + (y_f - y)^2}$
$\omega = k_\omega (\theta_d - \theta)$
où $\theta_d$ est l'angle désiré calculé comme :
$\theta_d = \arctan2(y_f - y, x_f - x)$
et $k_v$ et $k_\omega$ sont des gains de proportionnalité.

### Avantages et Limitations
**Avantages :**
- Plus réaliste que les modèles à intégrateur unique pour certains types de robots.
- Utilisé pour les robots différentiel (deux roues motrices) et les robots tricycle.

**Limitations :**
- Plus complexe à contrôler qu'un modèle à intégrateur unique.
- Les algorithmes de planification de trajectoire doivent prendre en compte les contraintes cinématiques du modèle unicycle.

Pour plus de détails, vous pouvez consulter des ressources pédagogiques et des articles scientifiques spécialisés en robotique et contrôle de systèmes, disponibles sur des plateformes comme [arXiv](https://arxiv.org/) et dans les manuels de robotique.