$(document).ready(function(){
    $("#chat-text").change(function() {

        var chatStr = document.getElementById("chat-text").value;
        //console.log(chatStr)
        
        var chatArr = chatStr.split('\n')
        //console.log(chatArr)
        
        var people = [];
        for(i = 0; i < chatArr.length; i++)
        {
            //sanitizing tmp
            //var tmp = chatArr[i].match(/\] [a-zA-Z ]*:/g);
            var tmp = chatArr[i].match(/\] [a-zA-Z]+[^:]*/g);
            tmp = tmp.toString();
            tmp = tmp.split("]").pop();
            tmp = tmp.replace(/:/g, "");
            $.trim(tmp);
            //tmp = tmp.replace(/[^a-zA-Z ]/g, "");

            console.log(tmp);

            var there = -1;
            
            for(var j = 0; j < people.length; j++)
            {
                //sanitizing people[j]
                people[j] = people[j].toString();
                tmp = tmp.split("]").pop();
                people[j] = people[j].replace(/:/g, "");
                $.trim(people[j]);
                //people[j] = people[j].replace(/[^a-zA-Z ]/g, "");

                if(tmp === people[j])
                {
                    there = 0;
                    break;
                }
            }
            
            if(there === -1)
                people.push(tmp);
        }

        var $personChoice = $("#person-choice");
        $personChoice.empty();
        $.each(people, function(index, value) {
            $personChoice.append("<option>" + value + "</option>");
        
        });
    
        $personChoice.append("<option>None of the above</option>");    

    });

});

