fetch('/api/model_versions')
    .then(response => response.json())
    .then(data => {
        const dropdown = document.getElementById('model_dropdown');
        data.forEach(model => {
            const optionElement = document.createElement('option');
            optionElement.text = model;
            dropdown.add(optionElement);
        });
    })
    .catch(error => console.error('Error fetching dropdown values:', error))

function predict() {
    const model = document.getElementById("model_dropdown").value;
    const bitterness_ibu = parseFloat(document.getElementById("bitterness_ibu").value);
    const st_Cold = document.getElementById("st_Cold").checked;
    const bs_American_StyleImperialStout = document.getElementById("bs_American_StyleImperialStout").checked;
    const pfn_Bittersweet = document.getElementById("pfn_Bittersweet").checked;
    const color_srm = parseFloat(document.getElementById("color_srm").value);

    if (!bitterness_ibu || !color_srm) {
        alert('Bitte fülle alle Eingabefelder aus!');
        return; // Beendet die Funktion frühzeitig, wenn ein Feld fehlt
    }

    const queryParams = new URLSearchParams({
        model:model,
        bitterness_ibu: bitterness_ibu,
        st_Cold: st_Cold,
        bs_American_StyleImperialStout: bs_American_StyleImperialStout,
        pfn_Bittersweet: pfn_Bittersweet,
        color_srm: color_srm
    });

    fetch(`/api/predict?${queryParams}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json()
            })
        .then(data => {
            document.getElementById('predictedAbv').innerHTML = 'Predicted ABV: ' + data['abv'];
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
}