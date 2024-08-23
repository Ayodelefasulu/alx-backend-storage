-- This script lists all bands with 'Glam rock' as their main style,
-- ranked by their longevity in years until 2022.

-- Select the band name and calculate the lifespan
SELECT band_name,
       (2022 - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
