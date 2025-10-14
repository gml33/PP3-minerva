// Función para obtener el CSRF token de las cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null; 
}

// Funciones para gestionar categorías
async function cargarCategorias() {
    try {
        const res = await fetch('/api/categorias/');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const categorias = await res.json();
        
        const tabla = document.getElementById('tabla-categorias');
        const selectFiltro = document.getElementById('filtroCategoria');
        const selectAsignar = document.getElementById('modalCategorias'); 

        tabla.innerHTML = '';
        selectFiltro.innerHTML = '<option value="">Todas</option>';
        selectAsignar.innerHTML = ''; 

        categorias.forEach(cat => {
            // Para la tabla de gestión
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><input class="form-control form-control-sm" value="${cat.nombre}" data-id="${cat.id}" /></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="actualizarCategoria(${cat.id})">💾</button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarCategoria(${cat.id})">🗑</button>
                </td>`;
            tabla.appendChild(row);

            // Para el select de filtro
            const optFiltro = document.createElement('option');
            optFiltro.value = cat.id;
            optFiltro.textContent = cat.nombre;
            selectFiltro.appendChild(optFiltro);

            // Para el select múltiple de asignación en el modal
            const optAsignar = document.createElement('option');
            optAsignar.value = cat.id;
            optAsignar.textContent = cat.nombre;
            selectAsignar.appendChild(optAsignar);
        });
    } catch (error) {
        console.error('Error al cargar categorías:', error);
        alert('Error al cargar las categorías. Consulta la consola para más detalles.');
    }
}

document.getElementById('form-nueva-categoria').addEventListener('submit', async e => {
    e.preventDefault();
    const nombre = document.getElementById('nombreCategoria').value.trim();
    if (!nombre) {
        alert('El nombre de la categoría no puede estar vacío.');
        return;
    }
    try {
        const res = await fetch('/api/categorias/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ nombre })
        });
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        document.getElementById('nombreCategoria').value = '';
        cargarCategorias();
    } catch (error) {
        console.error('Error al agregar categoría:', error);
        alert('Error al agregar categoría. Consulta la consola para más detalles.');
    }
});

async function actualizarCategoria(id) {
    const inputElement = document.querySelector(`#tabla-categorias input[data-id="${id}"]`);
    const valor = inputElement ? inputElement.value.trim() : '';

    if (!valor) {
        alert('El nombre de la categoría no puede estar vacío.');
        return;
    }

    try {
        const res = await fetch(`/api/categorias/${id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ nombre: valor })
        });
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        cargarCategorias();
    } catch (error) {
        console.error('Error al actualizar categoría:', error);
        alert('Error al actualizar categoría. Consulta la consola para más detalles.');
    }
}

async function eliminarCategoria(id) {
    if (!confirm('¿Estás seguro de que quieres eliminar esta categoría? Esto no se puede deshacer.')) return;
    try {
        const res = await fetch(`/api/categorias/${id}/`, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        cargarCategorias();
    } catch (error) {
        console.error('Error al eliminar categoría:', error);
        alert('Error al eliminar categoría. Consulta la consola para más detalles.');
    }
}

// Funciones para gestionar Links
async function cargarLinks() {
    const categoria = document.getElementById('filtroCategoria').value;
    const fechaInicio = document.getElementById('fechaInicio').value;
    const fechaFin = document.getElementById('fechaFin').value;
    
    let url = '/api/links/'; 
    const params = new URLSearchParams();

    if (fechaInicio) params.append('fecha_inicio', fechaInicio);
    if (fechaFin) params.append('fecha_fin', fechaFin);
    if (categoria) params.append('categoria_id', categoria); 

    if (params.toString()) {
        url += `?${params.toString()}`;
    }

    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const links = await res.json();
        const tbody = document.getElementById('tabla-links');
        tbody.innerHTML = '';

        if (links.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No se encontraron links con los filtros seleccionados.</td></tr>';
            return;
        }

        links.forEach(link => {
            const row = document.createElement('tr');
            let estadoTexto = '';
            let accionesHtml = '';

            if (link.estado === 'aprobado') {
                estadoTexto = '<span class="badge bg-success">APROBADO</span>';
                accionesHtml = `<button class="btn btn-sm btn-info btn-ver-editar" data-link-id="${link.id}" data-link-url="${link.url}" data-link-estado="${link.estado}">Ver/Editar</button>`;
            } else if (link.estado === 'descartado') {
                estadoTexto = '<span class="badge bg-danger">DESCARTADO</span>';
                accionesHtml = `<button class="btn btn-sm btn-info btn-ver-editar" data-link-id="${link.id}" data-link-url="${link.url}" data-link-estado="${link.estado}">Ver/Editar</button>`;
            } else { 
                estadoTexto = '<span class="badge bg-warning text-dark">PENDIENTE</span>';
                accionesHtml = `<button class="btn btn-sm btn-secondary btn-clasificar" data-link-id="${link.id}" data-link-url="${link.url}" data-link-estado="${link.estado}">📋 Clasificar</button>`;
            }
            
            let categoriasHtml = 'Sin categoría';
            if (link.categorias && link.categorias.length > 0) {
                categoriasHtml = link.categorias.map(c => `<span class="badge bg-secondary me-1">${c.nombre || c}</span>`).join('');
            }

            const fechaCarga = new Date(link.fecha_carga).toLocaleDateString('es-AR', {
                year: 'numeric', month: '2-digit', day: '2-digit'
            });

            row.innerHTML = `
                <td class="url-column"><a href="${link.url}" target="_blank" title="${link.url}">${link.url}</a></td>
                <td>${fechaCarga}</td>
                <td>${categoriasHtml}</td>
                <td>${estadoTexto}</td>
                <td>${accionesHtml}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error al cargar links:', error);
        alert('Error al cargar links. Consulta la consola para más detalles.');
    }
}

// Función para abrir el modal de edición/clasificación
async function abrirModal(id, url, estadoActual) {
    const modalEditarLinkElement = document.getElementById('modalEditarLink');
    const modalEditarLink = new bootstrap.Modal(modalEditarLinkElement);
    
    document.getElementById('editarLinkId').value = id; 
    document.getElementById('editarLinkUrl').textContent = url;
    
    const selectAsignar = document.getElementById('modalCategorias'); 
    
    // Deselecciona todas las opciones antes de cargar las categorías del link
    Array.from(selectAsignar.options).forEach(option => {
        option.selected = false;
    });

    // Obtener las categorías actuales del link específico
    try {
        const resLink = await fetch(`/api/links/${id}/`);
        if (!resLink.ok) {
            const errorData = await resLink.json().catch(() => ({ detail: 'Error desconocido' }));
            throw new Error(`Error al obtener link: ${resLink.status} - ${errorData.detail || JSON.stringify(errorData)}`);
        }
        const linkData = await resLink.json();
        
        // Asegúrate de que linkData.categorias es un array, incluso si está vacío o nulo
        const categoriasAsignadasIds = (linkData.categorias || []).map(cat => String(cat.id || cat)); 

        Array.from(selectAsignar.options).forEach(option => {
            if (categoriasAsignadasIds.includes(option.value)) {
                option.selected = true;
            }
        });

    } catch (error) {
        console.error('Error al cargar las categorías del link en el modal:', error);
        alert('Error al cargar las categorías del link: ' + error.message);
    }

    const btnAprobar = document.getElementById('btnAprobar');
    const btnRechazar = document.getElementById('btnRechazar');

    // Habilitar siempre los botones y el select para permitir la edición
    btnAprobar.disabled = false;
    btnRechazar.disabled = false;
    selectAsignar.disabled = false; 

    modalEditarLink.show();
}

// Event listener delegado para los botones de la tabla
document.getElementById('tabla-links').addEventListener('click', function(event) {
    if (event.target.classList.contains('btn-clasificar') || event.target.classList.contains('btn-ver-editar')) {
        const linkId = event.target.dataset.linkId;
        const linkUrl = event.target.dataset.linkUrl;
        const linkEstado = event.target.dataset.linkEstado;
        abrirModal(linkId, linkUrl, linkEstado);
    }
});

// Lógica para actualizar estado (Aprobar/Rechazar)
const btnAprobarLink = document.getElementById('btnAprobar');
const btnRechazarLink = document.getElementById('btnRechazar');

if (btnAprobarLink) {
    btnAprobarLink.addEventListener('click', () => actualizarEstadoLink('aprobado'));
} else {
    console.warn("Botón 'Aprobar' con ID 'btnAprobar' no encontrado en el JS.");
}

if (btnRechazarLink) {
    btnRechazarLink.addEventListener('click', () => actualizarEstadoLink('descartado'));
} else {
    console.warn("Botón 'Rechazar' con ID 'btnRechazar' no encontrado en el JS.");
}

async function actualizarEstadoLink(estado) {
    const id = document.getElementById('editarLinkId').value;
    // ¡CORRECCIÓN APLICADA AQUÍ!
    // Se cambia 'categorias' por 'categoria_ids' para que coincida con el Serializer de Django.
    const categoriasSeleccionadas = Array.from(document.getElementById('modalCategorias').selectedOptions).map(opt => parseInt(opt.value)); 
    
    try {
        const res = await fetch(`/api/links/${id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ estado, categoria_ids: categoriasSeleccionadas }) // <--- CAMBIO IMPORTANTE
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({ detail: 'Error desconocido' }));
            throw new Error(`Error al actualizar el link: ${res.status} - ${errorData.detail || JSON.stringify(errorData)}`);
        }

        await registrarAccion(estado, id);

        alert(`Link ${id} actualizado a ${estado} correctamente.`);
        const modalInstance = bootstrap.Modal.getInstance(document.getElementById('modalEditarLink'));
        if (modalInstance) {
            modalInstance.hide();
        }
        cargarLinks(); 
    } catch (error) {
        console.error('Error al actualizar el estado del link:', error);
        alert('Error al actualizar el link: ' + error.message);
    }
}

// Función para registrar actividad (opcional)
async function registrarAccion(tipo, id_link) {
    try {
        await fetch('/api/actividad/clic_link/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ url: `Acción ${tipo} en link ${id_link}` })
        });
    } catch (error) {
        console.warn('Advertencia: No se pudo registrar la acción de actividad:', error);
    }
}

// Event listener para el botón de filtrar
document.getElementById('btnFiltrar').addEventListener('click', cargarLinks);

// Cargar datos iniciales al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    cargarCategorias(); 
    cargarLinks();       
});