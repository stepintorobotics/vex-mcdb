function fetch_match() {
    fetch("http://127.0.0.1:5000/stats/52066/111877")
    .then(response => response.json())
    .then(data => {
        // If VRC, hide VIQC teams and vice versa
        if (data["season"] == 181) {
            document.getElementById("viqc").classList.add("hidden")
        } else {
            document.getElementById("vrc").classList.add("hidden")
        }

        document.getElementById("red1_points_total").innerHTML = "<br>Points scored (total): " + data["teams"].red1["points_total"]
        document.getElementById("red1_points_event").innerHTML = "Points scored (event): " + data["teams"].red1["points_event"]
    })
}