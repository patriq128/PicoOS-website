var table = document.getElementById("apps_table");

fetch("/download/apps/manifest.json")
    .then(function (res) {
        return res.json();
    })
    .then(function (data) {
        table.deleteRow(1);

        for (var file in data) {
            var row = table.insertRow();
            row.insertCell().textContent = file.replace(".pcs", "");
            row.insertCell().textContent = data[file].description;
            row.insertCell().textContent = data[file].author;
            row.insertCell().innerHTML = '<a href="/download/apps/' + file + '" download>download</a>';
        }
    })
    .catch(function (err) {
        console.log(err);
        table.rows[1].cells[0].textContent = "could not load apps";
    });