

console.log("加载了index.js文件")

let PROJECT = '';

function loadProjectManagement() {
    $.ajax({
    url: '/load-project',
    success: function (result) {
        PROJECT = result
        for (let j=0; j<result.project.length; j++) {
            let ele = `<option value=${result.project[j]}>${result.project[j]}</option>>`
            $("#project-select").append(ele)
        }
    }})
}


$(document).ready(function(){

    $('input[disabled="true"]').css("background", "darkgray")

    $('#project-select').change(function(){

        let project=$(this).children('option:selected').val();//这就是selected的值
        let idx = PROJECT.project.indexOf(project)
        $('input[name="sop"]').val(PROJECT.sop[idx])
        $('input[name="tma"]').val(PROJECT.tma[idx])
    })
})