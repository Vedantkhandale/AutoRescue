(function () {
    function showAlert(targetId, message, type) {
        const target = document.getElementById(targetId);
        if (!target) {
            return;
        }

        target.innerHTML = `
            <div class="alert alert-${type} mt-3" role="alert">
                ${message}
            </div>
        `;
    }

    async function parseResponse(response) {
        const contentType = response.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {
            return response.json();
        }
        const text = await response.text();
        throw new Error(text || "Unexpected response from server.");
    }

    async function submitForm(url, formData) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
        });

        const data = await parseResponse(response);
        if (!response.ok) {
            throw new Error(data.error || "Request failed.");
        }
        return data;
    }

    async function postJson(url, payload) {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            body: JSON.stringify(payload),
        });

        const data = await parseResponse(response);
        if (!response.ok) {
            throw new Error(data.error || "Request failed.");
        }
        return data;
    }

    function getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error("Geolocation is not supported in this browser."));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                    });
                },
                () => reject(new Error("Unable to capture current location.")),
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        });
    }

    function toast(message, type) {
        const existing = document.querySelector(".toast-shell");
        if (existing) {
            existing.remove();
        }

        const shell = document.createElement("div");
        shell.className = `toast-shell ${type || "success"}`;
        shell.textContent = message;
        document.body.appendChild(shell);

        window.setTimeout(() => {
            shell.remove();
        }, 2400);
    }

    window.AutoRescue = {
        showAlert,
        submitForm,
        postJson,
        getCurrentLocation,
        toast,
    };
})();
