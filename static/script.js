document.addEventListener('DOMContentLoaded', () => {

    // --- Tab Switching Logic ---
    const tabs = document.querySelectorAll('.tab-btn');
    const forms = document.querySelectorAll('.form-container');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));

            // Add active class
            tab.classList.add('active');
            const target = document.getElementById(`${tab.dataset.tab}-tab`);
            target.classList.add('active');
        });
    });

    // --- File Drag & Drop Logic ---
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('excel_file');
    const fileMessage = document.querySelector('.file-message');

    ['dragover', 'dragenter'].forEach(evt => {
        dropArea.addEventListener(evt, (e) => {
            e.preventDefault();
            dropArea.classList.add('is-dragover');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        dropArea.addEventListener(evt, (e) => {
            e.preventDefault();
            dropArea.classList.remove('is-dragover');
        });
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileMessage.innerHTML = `<i class="fa-solid fa-check" style="color:var(--clr-success)"></i> Selected: <strong>${fileInput.files[0].name}</strong>`;
        }
    });

    // --- Utility Methods ---
    const overlay = document.getElementById('loading-overlay');
    const showLoading = (show) => {
        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    };

    const syntaxHighlight = (json) => {
        if (typeof json != 'string') {
            json = JSON.stringify(json, undefined, 2);
        }
        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
            var cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        });
    }

    // --- Single URL Submission ---
    document.getElementById('single-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const publishedUrl = document.getElementById('published_url').value;
        const targetUrl = document.getElementById('target_url').value;
        const resultBox = document.getElementById('single-result');

        resultBox.classList.add('hidden');
        resultBox.className = 'result-box hidden'; // reset
        showLoading(true);

        try {
            const res = await fetch('/api/scrape/single', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    published_url: publishedUrl,
                    target_url: targetUrl
                })
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Failed to fetch data');
            }

            resultBox.innerHTML = `<strong>Results:</strong><br><pre>${syntaxHighlight(data.data)}</pre>`;
            resultBox.classList.add('success');
        } catch (err) {
            resultBox.innerHTML = `<strong>Error:</strong> ${err.message}`;
            resultBox.classList.add('error');
        } finally {
            resultBox.classList.remove('hidden');
            showLoading(false);
        }
    });

    // --- Excel Form Submission ---
    document.getElementById('excel-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            alert('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const statusBox = document.getElementById('excel-status');
        statusBox.classList.add('hidden');
        statusBox.className = 'status-box hidden';
        showLoading(true);

        try {
            const res = await fetch('/api/scrape/excel', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                let errData;
                try {
                    errData = await res.json();
                } catch (e) { errData = { detail: await res.text() } }
                throw new Error(errData.detail || 'Upload processing failed.');
            }

            // Download file
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scraped_results_${Date.now()}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            statusBox.innerHTML = `<i class="fa-solid fa-check-circle"></i> Successfully processed! Downloading the file...`;
            statusBox.classList.add('success');

        } catch (err) {
            statusBox.innerHTML = `<strong>Error:</strong> ${err.message}`;
            statusBox.classList.add('error');
        } finally {
            statusBox.classList.remove('hidden');
            showLoading(false);
        }
    });

    // --- Google Sheet Submission ---
    document.getElementById('sheet-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const sheetUrl = document.getElementById('sheet_url').value;
        const statusBox = document.getElementById('sheet-status');

        statusBox.classList.add('hidden');
        statusBox.className = 'status-box hidden';
        showLoading(true);

        const formData = new FormData();
        formData.append('sheet_url', sheetUrl);

        try {
            const res = await fetch('/api/scrape/sheet', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                let errData;
                try {
                    errData = await res.json();
                } catch (e) { errData = { detail: await res.text() } }
                throw new Error(errData.detail || 'Failed fetching Google Sheet.');
            }

            // Download file
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scraped_results_sheet_${Date.now()}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            statusBox.innerHTML = `<i class="fa-solid fa-check-circle"></i> Successfully fetched and processed Google Sheet! Downloading the file...`;
            statusBox.classList.add('success');

        } catch (err) {
            statusBox.innerHTML = `<strong>Error:</strong> ${err.message}`;
            statusBox.classList.add('error');
        } finally {
            statusBox.classList.remove('hidden');
            showLoading(false);
        }
    });

});
