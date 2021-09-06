
//function for log.html.
function getInputCalorie(){
    var weiVal=document.getElementById('WeightInput').value;
    //document.getElementById('pasteResult').innerHTML=weitVal;

    var walkVal = document.getElementById('walkInput').value;
    //document.getElementById('pasteResult').innerHTML=walkVal;

    var runVal = document.getElementById('runInput').value;
    //document.getElementById('pasteResult').innerHTML=runVal;

    var swimVal = document.getElementById('swimInput').value;
    //document.getElementById('pasteResult').innerHTML=swimVal;

    var bicyVal = document.getElementById('bicyInput').value;
    //document.getElementById('pasteResult').innerHTML=bicyVal;

    //formula: (duration * MET) *(3.5 *Weight)/200
    //var formulaMET = (3.5 * parseInt(weiVal))/200; 
    var walkAns = parseInt(walkVal) //walking.
    var runAns = parseInt(runVal) //running.
    var swimAns = parseInt(swimVal) //swimming.
    var bicyAns = parseInt(bicyVal) //bicycling.
    
    //testing to get date time and display out.
    //var date=document.getElementById("dateTimeInput").value;
    //document.getElementById('pasteResult01').innerHTML=date;

    //pass value into function for ajax.
    postInputCalorieViaAjax(weiVal,walkAns,runAns, swimAns,bicyAns);
}


//function log.html for ajax to get data from getInputCalorie() and send to flask.
function postInputCalorieViaAjax(weiVal,walkAns,runAns, swimAns,bicyAns){
    $.ajax({    
        type: 'POST',
        data: JSON.stringify({'weiVal':weiVal,'walkAns': walkAns, 'runAns': runAns, 'swimAns': swimAns, 'bicyAns': bicyAns}),
        contentType: "application/json",
        dataType: 'json',
        url: '/logPage', 
    }).done(function (input){
        if (input.error){
            console.log(input.error)
        }else{ 

            //testing display calorie result from flask.
            console.log(input.calorieResult)
            var showsResult = input.calorieResult

            //convert back to int for display out.
            document.getElementById('pasteResult').innerHTML= parseInt(showsResult).toFixed(0) ;
        }} 
    )  
}