TokenPosPosFM <- ((avgtokenprecPP * avgtokenrecallPP) / 
     (avgtokenprecPP + avgtokenrecallPP)) * 2

CategoryPosPosFM <- ((avgcatprecPP * avgcatrecallPP) /
     (avgcatprecPP + avgcatrecallPP)) * 2

TokenPosNegFM <- ((avgtokenprecPN * avgtokenrecallPN) /
     (avgtokenprecPN + avgtokenrecallPN)) * 2

CategoryPosNegFM <- ((avgcatprecPN * avgcatrecallPN) /
     (avgcatprecPN + avgcatrecallPN)) * 2
