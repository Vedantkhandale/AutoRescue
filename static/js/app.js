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

    function setButtonLoading(button, label) {
        if (!button) {
            return () => {};
        }

        const originalContent = button.innerHTML;
        button.disabled = true;
        button.innerHTML = `<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>${label}`;

        return () => {
            button.disabled = false;
            button.innerHTML = originalContent;
        };
    }

    function initMotionSystem() {
        const selectors = [
            ".confidence-grid > div",
            ".workflow-showcase",
            ".workflow-lane",
            ".role-feature-card",
            ".rescue-steps li",
            ".rescue-cta-card",
            ".dashboard-card",
            ".dashboard-workflow-panel",
            ".workflow-progress-step",
            ".ops-command-grid > div",
            ".job-card",
            ".request-row",
            ".auth-aside",
            ".auth-card",
            ".rescue-guidance-card",
            ".rescue-form-card",
            ".empty-state",
        ];
        const targets = Array.from(document.querySelectorAll(selectors.join(",")));
        if (!targets.length) {
            return;
        }

        document.documentElement.classList.add("motion-ready");
        const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        targets.forEach((target, index) => {
            target.classList.add("motion-reveal");
            target.style.setProperty("--reveal-delay", `${(index % 8) * 70}ms`);
        });

        if (prefersReducedMotion || !("IntersectionObserver" in window)) {
            targets.forEach((target) => target.classList.add("is-visible"));
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) {
                        return;
                    }
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                });
            },
            { threshold: 0.14, rootMargin: "0px 0px -8% 0px" }
        );

        targets.forEach((target) => observer.observe(target));
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initMotionSystem);
    } else {
        initMotionSystem();
    }

    window.AutoRescue = {
        showAlert,
        submitForm,
        postJson,
        getCurrentLocation,
        toast,
        setButtonLoading,
    };
})();
