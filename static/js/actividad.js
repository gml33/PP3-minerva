document.addEventListener("DOMContentLoaded", () => {
    const tablaBody = document.getElementById("tabla-actividad");
    const filtroForm = document.getElementById("filtro-actividad");
    const usuarioSelect = document.getElementById("usuario");
    const tipoSelect = document.getElementById("tipo");
    const desdeInput = document.getElementById("desde");
    const hastaInput = document.getElementById("hasta");

    cargarUsuarios();
    cargarTipos();
    cargarActividades(); // carga inicial sin filtros

    filtroForm.addEventListener("submit", e => {
        e.preventDefault();
        cargarActividades();
    });

    document.getElementById("btnExportar").addEventListener("click", () => {
        let url = "http://127.0.0.1:8000/api/actividades/exportar_excel/?";

        const filtros = [];
        if (usuarioSelect.value) filtros.push(`usuario=${usuarioSelect.value}`);
        if (tipoSelect.value) filtros.push(`tipo=${tipoSelect.value}`);
        if (desdeInput.value) filtros.push(`desde=${desdeInput.value}`);
        if (hastaInput.value) filtros.push(`hasta=${hastaInput.value}`);

        if (filtros.length > 0) {
            url += filtros.join("&");
        }

        window.open(url, "_blank");  // abre o descarga el Excel
    });

    document.getElementById("btnExportarPDF").addEventListener("click", () => {
        let url = "http://127.0.0.1:8000/api/actividades/exportar_pdf/?";

        const filtros = [];
        if (usuarioSelect.value) filtros.push(`usuario=${usuarioSelect.value}`);
        if (tipoSelect.value) filtros.push(`tipo=${tipoSelect.value}`);
        if (desdeInput.value) filtros.push(`desde=${desdeInput.value}`);
        if (hastaInput.value) filtros.push(`hasta=${hastaInput.value}`);

        if (filtros.length > 0) {
            url += filtros.join("&");
        }

        window.open(url, "_blank");
    });

    async function cargarUsuarios() {
        const res = await fetch("http://127.0.0.1:8000/api/usuarios/");
        const data = await res.json();
        data.forEach(user => {
            const option = document.createElement("option");
            option.value = user.username;
            option.textContent = `${user.username}`;
            usuarioSelect.appendChild(option);
        });
    }

    function cargarTipos() {
        const tipos = {
            login: "Inicio de sesión",
            logout: "Cierre de sesión",
            carga_link: "Carga de Link",
            cambio_estado: "Cambio de Estado",
            clic_link: "Clic en Link",
            creacion_articulo: "Creación de Artículo",
            otro: "Otro"
        };
        for (let key in tipos) {
            const option = document.createElement("option");
            option.value = key;
            option.textContent = tipos[key];
            tipoSelect.appendChild(option);
        }
    }

    async function cargarActividades() {
        tablaBody.innerHTML = "";

        let url = "http://127.0.0.1:8000/api/actividades/?";

        const filtros = [];
        if (usuarioSelect.value) filtros.push(`usuario=${usuarioSelect.value}`);
        if (tipoSelect.value) filtros.push(`tipo=${tipoSelect.value}`);
        if (desdeInput.value) filtros.push(`desde=${desdeInput.value}`);
        if (hastaInput.value) filtros.push(`hasta=${hastaInput.value}`);

        if (filtros.length > 0) {
            url += filtros.join("&");
        }

        const res = await fetch(url);
        const data = await res.json();

        console.log("Actividades recibidas:", data);

        if (data.length === 0) {
            tablaBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center text-muted">No se encontraron actividades con los filtros aplicados.</td>
                </tr>
            `;
            return;
        }

        data.forEach(act => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${new Date(act.fecha_hora).toLocaleString()}</td>
                <td>${act.usuario || '(anónimo)'}</td>
                <td>${act.tipo.replaceAll('_', ' ')}</td>
                <td>${act.descripcion}</td>
            `;
            tablaBody.appendChild(row);
        });
    }
});