let award, awards, award_item, award_list, award_name, award_event;

function fetch_match() {
    fetch("http://127.0.0.1:5000/stats/52066/111877")
    .then(response => response.json())
    .then(data => {
        // If VRC, hide VIQC teams and vice versa
        if (data["season"] == 181) {
            document.getElementById("viqc").classList.add("hidden");
        } else {
            document.getElementById("vrc").classList.add("hidden");
        }

        // Insert data for VRC teams
        document.getElementById("red1_number").innerHTML = "<br><br><b>" + data["teams"].red1["team_number"] + "</b>";
        document.getElementById("red1_name").innerHTML = data["teams"].red1["team_name"];
        document.getElementById("red1_grade").innerHTML = "<br>" + data["teams"].red1["team_grade"];
        document.getElementById("red1_organisation").innerHTML = data["teams"].red1["team_organisation"];
        document.getElementById("red1_city").innerHTML = data["teams"].red1["team_city"];
        document.getElementById("red1_robot").innerHTML = "<br>Robot: " + data["teams"].red1["team_robot"];
        document.getElementById("red1_matches_total").innerHTML = "<br>Matches played (total): " + data["teams"].red1["matches_total"];
        document.getElementById("red1_wins_total").innerHTML = "Matches won (total): " + data["teams"].red1["wins_total"];
        document.getElementById("red1_wins_pct_total").innerHTML = "Win % (total): " + data["teams"].red1["wins_pct_total"];
        document.getElementById("red1_matches_event").innerHTML = "<br>Matches played (event): " + data["teams"].red1["matches_event"];
        document.getElementById("red1_wins_event").innerHTML = "Matches won (event): " + data["teams"].red1["wins_event"];
        document.getElementById("red1_wins_pct_event").innerHTML = "Win % (event): " + data["teams"].red1["wins_pct_event"];
        document.getElementById("red1_points_total").innerHTML = "<br>Points scored (total): " + data["teams"].red1["points_total"];
        document.getElementById("red1_points_avg_total").innerHTML = "Average points (total): " + data["teams"].red1["points_avg_total"];
        document.getElementById("red1_points_event").innerHTML = "<br>Points scored (event): " + data["teams"].red1["points_event"];
        document.getElementById("red1_points_avg_event").innerHTML = "Average points (event): " + data["teams"].red1["points_avg_event"];
        document.getElementById("red1_hs_total_score").innerHTML = "<br>High score (total): " + data["teams"].red1["team_hs_total"];
        document.getElementById("red1_hs_total_match").innerHTML = data["teams"].red1["team_hs_total_match"][0];
        document.getElementById("red1_hs_total_event").innerHTML = data["teams"].red1["team_hs_total_match"][1];
        document.getElementById("red1_hs_event_score").innerHTML = "<br>High score (total): " + data["teams"].red1["team_hs_event"];
        document.getElementById("red1_hs_event_match").innerHTML = data["teams"].red1["team_hs_event_match"];
        document.getElementById("red1_awards").innerHTML = data["teams"].red1["awards"];
        awards = data["teams"].red1["awards"];
        award_list = document.getElementById("red1_awards");
        award_list.innerHTML = "<br>";
        for (award of awards) {
            award_item = document.createElement("li");
            award_item.innerHTML = "<b>" + award[0] + "</b><br>" + award[1];
            award_list.appendChild(award_item);
        }
    })
}

fetch_match();