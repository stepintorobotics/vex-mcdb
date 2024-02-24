let award, awards, award_item, award_list, award_name, award_event;
let target_div, target_inst, target_num, target_type, endpoint;
let target_event = 52066;
let url_base = "http://127.0.0.1:5000/"

function fetch_match(team1, team2, team3, team4, event_name, match_name) {
    fetch(url_base + "stats/" + target_event + "/" + team1 + "/" + team2 + "/" + team3 + "/" + team4)
    .then(response => response.json())
    .then(data => {
        // If VRC, hide VIQC teams and vice versa
        if (data["season"] == 181) {
            document.getElementById("viqc").classList.add("hidden");
        } else {
            document.getElementById("vrc").classList.add("hidden");
        }

        // Insert match information
        document.getElementById("event_name").innerHTML = event_name;
        document.getElementById("match_name").innerHTML = "<br><b>" + match_name + "</b>"

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
        document.getElementById("red1_hs_event_score").innerHTML = "<br>High score (event): " + data["teams"].red1["team_hs_event"];
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

        document.getElementById("red2_number").innerHTML = "<br><br><b>" + data["teams"].red2["team_number"] + "</b>";
        document.getElementById("red2_name").innerHTML = data["teams"].red2["team_name"];
        document.getElementById("red2_grade").innerHTML = "<br>" + data["teams"].red2["team_grade"];
        document.getElementById("red2_organisation").innerHTML = data["teams"].red2["team_organisation"];
        document.getElementById("red2_city").innerHTML = data["teams"].red2["team_city"];
        document.getElementById("red2_robot").innerHTML = "<br>Robot: " + data["teams"].red2["team_robot"];
        document.getElementById("red2_matches_total").innerHTML = "<br>Matches played (total): " + data["teams"].red2["matches_total"];
        document.getElementById("red2_wins_total").innerHTML = "Matches won (total): " + data["teams"].red2["wins_total"];
        document.getElementById("red2_wins_pct_total").innerHTML = "Win % (total): " + data["teams"].red2["wins_pct_total"];
        document.getElementById("red2_matches_event").innerHTML = "<br>Matches played (event): " + data["teams"].red2["matches_event"];
        document.getElementById("red2_wins_event").innerHTML = "Matches won (event): " + data["teams"].red2["wins_event"];
        document.getElementById("red2_wins_pct_event").innerHTML = "Win % (event): " + data["teams"].red2["wins_pct_event"];
        document.getElementById("red2_points_total").innerHTML = "<br>Points scored (total): " + data["teams"].red2["points_total"];
        document.getElementById("red2_points_avg_total").innerHTML = "Average points (total): " + data["teams"].red2["points_avg_total"];
        document.getElementById("red2_points_event").innerHTML = "<br>Points scored (event): " + data["teams"].red2["points_event"];
        document.getElementById("red2_points_avg_event").innerHTML = "Average points (event): " + data["teams"].red2["points_avg_event"];
        document.getElementById("red2_hs_total_score").innerHTML = "<br>High score (total): " + data["teams"].red2["team_hs_total"];
        document.getElementById("red2_hs_total_match").innerHTML = data["teams"].red2["team_hs_total_match"][0];
        document.getElementById("red2_hs_total_event").innerHTML = data["teams"].red2["team_hs_total_match"][1];
        document.getElementById("red2_hs_event_score").innerHTML = "<br>High score (event): " + data["teams"].red2["team_hs_event"];
        document.getElementById("red2_hs_event_match").innerHTML = data["teams"].red2["team_hs_event_match"];
        document.getElementById("red2_awards").innerHTML = data["teams"].red2["awards"];
        awards = data["teams"].red2["awards"];
        award_list = document.getElementById("red2_awards");
        award_list.innerHTML = "<br>";
        for (award of awards) {
            award_item = document.createElement("li");
            award_item.innerHTML = "<b>" + award[0] + "</b><br>" + award[1];
            award_list.appendChild(award_item);
        }

        document.getElementById("blue1_number").innerHTML = "<br><br><b>" + data["teams"].blue1["team_number"] + "</b>";
        document.getElementById("blue1_name").innerHTML = data["teams"].blue1["team_name"];
        document.getElementById("blue1_grade").innerHTML = "<br>" + data["teams"].blue1["team_grade"];
        document.getElementById("blue1_organisation").innerHTML = data["teams"].blue1["team_organisation"];
        document.getElementById("blue1_city").innerHTML = data["teams"].blue1["team_city"];
        document.getElementById("blue1_robot").innerHTML = "<br>Robot: " + data["teams"].blue1["team_robot"];
        document.getElementById("blue1_matches_total").innerHTML = "<br>Matches played (total): " + data["teams"].blue1["matches_total"];
        document.getElementById("blue1_wins_total").innerHTML = "Matches won (total): " + data["teams"].blue1["wins_total"];
        document.getElementById("blue1_wins_pct_total").innerHTML = "Win % (total): " + data["teams"].blue1["wins_pct_total"];
        document.getElementById("blue1_matches_event").innerHTML = "<br>Matches played (event): " + data["teams"].blue1["matches_event"];
        document.getElementById("blue1_wins_event").innerHTML = "Matches won (event): " + data["teams"].blue1["wins_event"];
        document.getElementById("blue1_wins_pct_event").innerHTML = "Win % (event): " + data["teams"].blue1["wins_pct_event"];
        document.getElementById("blue1_points_total").innerHTML = "<br>Points scored (total): " + data["teams"].blue1["points_total"];
        document.getElementById("blue1_points_avg_total").innerHTML = "Average points (total): " + data["teams"].blue1["points_avg_total"];
        document.getElementById("blue1_points_event").innerHTML = "<br>Points scored (event): " + data["teams"].blue1["points_event"];
        document.getElementById("blue1_points_avg_event").innerHTML = "Average points (event): " + data["teams"].blue1["points_avg_event"];
        document.getElementById("blue1_hs_total_score").innerHTML = "<br>High score (total): " + data["teams"].blue1["team_hs_total"];
        document.getElementById("blue1_hs_total_match").innerHTML = data["teams"].blue1["team_hs_total_match"][0];
        document.getElementById("blue1_hs_total_event").innerHTML = data["teams"].blue1["team_hs_total_match"][1];
        document.getElementById("blue1_hs_event_score").innerHTML = "<br>High score (event): " + data["teams"].blue1["team_hs_event"];
        document.getElementById("blue1_hs_event_match").innerHTML = data["teams"].blue1["team_hs_event_match"];
        document.getElementById("blue1_awards").innerHTML = data["teams"].blue1["awards"];
        awards = data["teams"].blue1["awards"];
        award_list = document.getElementById("blue1_awards");
        award_list.innerHTML = "<br>";
        for (award of awards) {
            award_item = document.createElement("li");
            award_item.innerHTML = "<b>" + award[0] + "</b><br>" + award[1];
            award_list.appendChild(award_item);
        }

        document.getElementById("blue2_number").innerHTML = "<br><br><b>" + data["teams"].blue2["team_number"] + "</b>";
        document.getElementById("blue2_name").innerHTML = data["teams"].blue2["team_name"];
        document.getElementById("blue2_grade").innerHTML = "<br>" + data["teams"].blue2["team_grade"];
        document.getElementById("blue2_organisation").innerHTML = data["teams"].blue2["team_organisation"];
        document.getElementById("blue2_city").innerHTML = data["teams"].blue2["team_city"];
        document.getElementById("blue2_robot").innerHTML = "<br>Robot: " + data["teams"].blue2["team_robot"];
        document.getElementById("blue2_matches_total").innerHTML = "<br>Matches played (total): " + data["teams"].blue2["matches_total"];
        document.getElementById("blue2_wins_total").innerHTML = "Matches won (total): " + data["teams"].blue2["wins_total"];
        document.getElementById("blue2_wins_pct_total").innerHTML = "Win % (total): " + data["teams"].blue2["wins_pct_total"];
        document.getElementById("blue2_matches_event").innerHTML = "<br>Matches played (event): " + data["teams"].blue2["matches_event"];
        document.getElementById("blue2_wins_event").innerHTML = "Matches won (event): " + data["teams"].blue2["wins_event"];
        document.getElementById("blue2_wins_pct_event").innerHTML = "Win % (event): " + data["teams"].blue2["wins_pct_event"];
        document.getElementById("blue2_points_total").innerHTML = "<br>Points scored (total): " + data["teams"].blue2["points_total"];
        document.getElementById("blue2_points_avg_total").innerHTML = "Average points (total): " + data["teams"].blue2["points_avg_total"];
        document.getElementById("blue2_points_event").innerHTML = "<br>Points scored (event): " + data["teams"].blue2["points_event"];
        document.getElementById("blue2_points_avg_event").innerHTML = "Average points (event): " + data["teams"].blue2["points_avg_event"];
        document.getElementById("blue2_hs_total_score").innerHTML = "<br>High score (total): " + data["teams"].blue2["team_hs_total"];
        document.getElementById("blue2_hs_total_match").innerHTML = data["teams"].blue2["team_hs_total_match"][0];
        document.getElementById("blue2_hs_total_event").innerHTML = data["teams"].blue2["team_hs_total_match"][1];
        document.getElementById("blue2_hs_event_score").innerHTML = "<br>High score (event): " + data["teams"].blue2["team_hs_event"];
        document.getElementById("blue2_hs_event_match").innerHTML = data["teams"].blue2["team_hs_event_match"];
        document.getElementById("blue2_awards").innerHTML = data["teams"].blue2["awards"];
        awards = data["teams"].blue2["awards"];
        award_list = document.getElementById("blue2_awards");
        award_list.innerHTML = "<br>";
        for (award of awards) {
            award_item = document.createElement("li");
            award_item.innerHTML = "<b>" + award[0] + "</b><br>" + award[1];
            award_list.appendChild(award_item);
        }
    })
}

document.getElementById("refresh").addEventListener("click", function(){
    target_div = Number(document.getElementById("selected_div").value);
    target_type = Number(document.getElementById("selected_type").value);
    target_inst = Number(document.getElementById("selected_inst").value);
    target_num = Number(document.getElementById("selected_num").value);
    endpoint = url_base + "match/" + target_event + "/" + target_div + "/" + target_type + "/" + target_inst + "/" + target_num;
    fetch(endpoint)
    .then(response => response.json())
    .then(data => {
        fetch_match(data[0][0], data[0][1], data[0][2], data[0][3], data[0][5], data[0][4]);
    })
});