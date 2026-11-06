# Herramientas de The Fragrance Club

Respaldo de los scripts que actualizan la tienda. No contiene costos, clientes ni ventas.

- `sync.py`: genera el catálogo público desde el inventario interno.
- `seo.py`: genera logo de pestaña, páginas por perfume y colección, sitemap y datos para Google.
- `tfc-trazo.txt`: trazo del logo para el ícono del sitio.

El inventario interno (costos, ventas, clientes) vive en la página interna del equipo, nunca en este repositorio.

Para restaurar en un espacio nuevo: copiar estos archivos a `/home/claude/tienda/`, el `data.json` de la página interna a `/home/claude/perfumes/data.json`, `data.json` de este repositorio a `/home/claude/tienda/data.json`, `img/` a `/home/claude/img/`, y clonar este repositorio en `/home/claude/the-fragrance-club`.
