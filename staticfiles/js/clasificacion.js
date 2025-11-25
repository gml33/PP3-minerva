document.addEventListener("DOMContentLoaded", () => {
    const tablaBody = document.querySelector("#tabla-links tbody");
    const filtroForm = document.getElementById("filtro-form");
    const fechaInicio = document.getElementById("fechaInicio");
    const fechaFin = document.getElementById("fechaFin");

    if (!tablaBody || !filtroForm) return;

    filtroForm.addEventListener("submit", e => {
        e.preventDefault();
        cargarLinksClasificacion();
    });

    async function cargarLinksClasificacion() {
        tablaBody.innerHTML = "";

        let url = "http://127.0.0.1:8000/api/links/";
        const params = [];

        if (fechaInicio.value) params.push(`fecha_inicio=${fechaInicio.value}`);
        if (fechaFin.value) params.push(`fecha_fin=${fechaFin.value}`);

        if (params.length > 0) {
            url += "?" + params.join("&");
        }

        const res = await fetch(url);
        const data = await res.json();

        data.forEach(link => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>
                    <a href="${link.url}" target="_blank" class="link-clic" data-url="${link.url}">
                        ${link.url}
                    </a>
                </td>
                <td>${new Date(link.fecha_carga).toLocaleDateString()}</td>
                <td>${link.cargado_por}</td>
                <td>
                    <select class="form-select form-select-sm estado-select" data-id="${link.id}">
                        <option value="pendiente" ${link.estado === "pendiente" ? "selected" : ""}>Pendiente</option>
                        <option value="aprobado" ${link.estado === "aprobado" ? "selected" : ""}>Aprobado</option>
                        <option value="descartado" ${link.estado === "descartado" ? "selected" : ""}>Descartado</option>
                    </select>
                </td>
                <td>
                    <button class="btn btn-sm btn-success actualizar-btn" data-id="${link.id}">Actualizar</button>
                    <div id="mensaje-${link.id}" class="text-success small mt-1" style="display:none;">✅ Actualizado</div>
                </td>
            `;

            tablaBody.appendChild(row);
        });

        // Clic en links: registrar actividad
        setTimeout(() => {
            document.querySelectorAll(".link-clic").forEach(enlace => {
                enlace.addEventListener("click", e => {
                    const url = e.currentTarget.dataset.url;

                    fetch("http://127.0.0.1:8000/api/actividad/clic_link/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken")
                        },
                        body: JSON.stringify({ url })
                    });
                });
            });
        }, 100);

        // Evento de actualización
        document.querySelectorAll(".actualizar-btn").forEach(button => {
            button.addEventListener("click", async function () {
                const linkId = this.dataset.id;
                const select = document.querySelector(`select.estado-select[data-id="${linkId}"]`);
                const nuevoEstado = select.value;

                const response = await fetch(`http://127.0.0.1:8000/api/links/${linkId}/`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: JSON.stringify({ estado: nuevoEstado })
                });

                const respuestaTexto = await response.text();

                if (response.ok) {
                    const msg = document.getElementById(`mensaje-${linkId}`);
                    msg.style.display = "block";
                    msg.textContent = "✅ Actualizado";
                    setTimeout(() => msg.style.display = "none", 2000);
                } else {
                    alert("❌ Error al actualizar el estado:\n" + respuestaTexto);
                }
            });
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    cargarLinksClasificacion();
});