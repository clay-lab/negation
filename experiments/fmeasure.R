TokenPosPosFM <- 2 * 
  ((avgtokenprecPP * avgtokenrecallPP) / 
     (avgtokenprecPP + avgtokenrecallPP))

CategoryPosPosFM <- 2 * 
  ((avgcatprecPP * avgcatrecallPP) /
     (avgcatprecPP + avgcatrecallPP))

TokenPosNegFM <- 2 *
  ((avgtokenprecPN * avgtokenrecallPN) /
     (avgtokenprecPN + avgtokenrecallPN))

CategoryPosNegFM <- 2 *
  ((avgcatprecPN * avgcatrecallPN) /
     (avgcatprecPN + avgcatrecallPN))
