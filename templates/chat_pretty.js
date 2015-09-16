$(document).ready(function(){
    $("#chat-text").change(function() {

        if("Foo:" == "Foo:")
            console.log("Yay");
        //some regex stuff goes here
        //var nEx = '(?<= )[a-zA-Z]+[^:]*'; 
        var chatStr = document.getElementById("chat-text").value;
        console.log(chatStr)
        
        var chatArr = chatStr.split('\n')
        console.log(chatArr)
        
        var people = new Array();
        for(i = 0; i < chatArr.length; i++)
        {
            var tmp = chatArr[i].match(/[a-zA-Z]+:/g);
            //var there = $.inArray(tmp, people);
            
            var there = -1;
            for(var j = 0; j < people.length; j++)
            {
                console.log(tmp);
                console.log(people[j]);
                console.log(tmp == people[j]);
                if(tmp === people[j])
                {
                    there = 0;
                    break;
                }
            }

            console.log(there);
            
            if(there === -1)
            {
                console.log("Not there.");
                people.push(tmp);
                for(j = 0; j < people.length; j++)
                    console.log(people[j]);
            }
        }

        var $personChoice = $("#person-choice");
        $personChoice.empty();
        $.each(people, function(index, value) {
            $personChoice.append("<option>" + value + "</option>");
        
        });
    
        $personChoice.append("<option>None of the above</option>");    

    });

});
