/* Javascript for MyXBlock. */

function MyXBlock(runtime, element) {


    function updateCount(result) {

        console.log(result);
        if(result.result==true)
         {

          $('.action-submit', element).val("已提交");
          
         }
        else
         {
          console.log(result);
         }
    }
    function update(result){
        console.log(result);
        window.location.reload(true);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');
    var studiosubmit = runtime.handlerUrl(element, 'studio_submit');
    var studentsubmit = runtime.handlerUrl(element, 'student_submit');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

     $('.student', element).click( function(){
       alert("test1");
       console.log("ttesta");
       $.ajax({
            type: "POST",
            url: studentsubmit,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
         });
    });

    $('.action-submit', element).click( function(){

     
    var $questions= $("section.quiz", element).find(".question").find(".question-content").find("input[type=radio], input[type=checkbox]");
   /* var $text= $("section.quiz", element).find(".question").find(".question-content").find("input[type=text]");*/
    var $area= $(".active-code", element).find("textarea");
    var $text=$("section.normal", element).find("input[type=text]");
    tk=""
    answer=""
    wd=""
    if($area)
     {
       $area.each(function(k){
                    wd+=$(this).val();
                  });

     }
    if($text)
      {
         $text.each(function(j){
                    tk+=$(this).val()+'|';
                  });
      }
    if($questions){
       $questions.each(function(i) {
                    if($(this).is(":checked"))
                    {
                      console.log(i);
                      if(i==0)
                       answer +='A';
                      if(i==1)
                       answer +='B';
                      if(i==2)
                       answer +='C';
                      if(i==3)
                       answer +='D';
                      if(i==4)
                       answer +='E';
                      if(i==5)
                       answer +='F';
                      if(i==6)
                       answer +='G';
                      if(i==7)
                       answer +='H';
                      if(i==8)
                       answer +='I';
                      if(i==9)
                       answer +='J';
                    } 
                }) ;    
  }

   if(wd!="")
   {
    $(this, element).val("正在提交...");
    $(this, element).attr("disabled",true);
    
    $.ajax({
            type: "POST",
            url: studentsubmit,
            data: JSON.stringify({"answer":wd}),
            success: updateCount
       });
   }

  if(tk!="")
   {
    $(this, element).val("正在提交...");
    $(this, element).attr("disabled",true);
    newtk=tk.substring(0, tk.length-1);

    $.ajax({
            type: "POST",
            url: studentsubmit,
            data: JSON.stringify({"answer":newtk}),
            success: updateCount
       });
   }


  if(answer!="")
   {
   $(this, element).val("正在提交...");
   $(this, element).attr("disabled",true);
    console.log(answer);
    $.ajax({
            type: "POST",
            url: studentsubmit,
            data: JSON.stringify({"answer":answer}),
            success: updateCount
       });
   }


 });


    $('.save-button', element).bind('click', function(){
        var params = { "src": $('input[name=src]', element).val()};
        
        $.ajax({
              type:"POST",
              url:studiosubmit,
              data: JSON.stringify(params),
              success:update
         });
       
           
   });

    $('.cancel-button', element).bind('click', function(){
        console.log("cancel");
         runtime.notify('cancel', {});
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
       sh_highlightDocument(); 
        }); 
}
