$(document).ready(function(){

    document.getElementById('error-text').style.visibility = "hidden";
    $('#submit-button').prop('disabled', true);
    //$('#person-choice').prop('disabled', true);
    
    $("#chat-text").change(function() {

        var chatStr = document.getElementById("chat-text").value;
        //console.log(chatStr)
        $.trim(chatStr);
        
        var chatArr = chatStr.split('\n')
     //console.log(chatArr)

        var sanitize = function(inptStr){
             inptStr = inptStr.toString();
             inptStr = inptStr.split("]").pop();
             inptStr = inptStr.replace(/:/g, "");
             $.trim(inptStr);
             return inptStr;
        }



         var people = [];
         for(i = 0; i < chatArr.length; i++)
         {
             var dateTime = chatArr[i].match(/\[[0-9][0-9]\/[0-9][0-9] [0-9][0-9]:[0-9][0-9]\]/g);
             console.log(dateTime);
             if(dateTime != null)
             {
                 //sanitizing tmp
                 var tmp = chatArr[i].match(/\] [a-zA-Z]+[^:]*/g);
                 tmp = sanitize(tmp);
                 console.log(tmp);

                 var there = -1;
                 
                 for(var j = 0; j < people.length; j++)
                 {
                     //sanitizing people[j]
                     people[j] = sanitize(people[j]);
                     console.log(people[j]);

                     if(tmp === people[j])
                     {
                         there = 0;
                         break;
                     }
                 }
                 
                 if(there === -1)
                     people.push(tmp);
             }
         }

         if(chatArr[0].match(/\[[0-9][0-9]\/[0-9][0-9] [0-9][0-9]:[0-9][0-9]\]/g) != null)
         { 
             
             var $personChoice = $("#person-choice");
             $personChoice.empty();
             $.each(people, function(index, value) {
                 $personChoice.append("<option>" + value + "</option>");
             
             });
         
             $personChoice.append("<option>None of the above</option>"); 
             
             document.getElementById('error-text').style.visibility = "hidden";
             $('#submit-button').prop('disabled', false);
             //$('#person-choice').prop('disabled', false);

         } 
         else
         {
             document.getElementById('error-text').style.visibility = "visible";
             $('#submit-button').prop('disabled', true);
             //$('#person-choice').prop('disabled', true);

         }
    });
});

