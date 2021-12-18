

function loadProjectInformation () {
    let project = $('input[name="project"]').val()
    let lingjianhao = $('input[name="lingjianhao"]').val()

    if (project === '' || lingjianhao === '') {
        alert("请输入要查询的项目名或者零件号！！！")
    } else {
        $.ajax({
        data: {project: project, lingjianhao: lingjianhao},
        url: '/load-project-information',
        success: function (result) {
            let keys_ = result.data.keys
            let items = result.data.items
            if(items) {
                $('#nullData').remove()
                for (let i=0; i<keys_.length; i++) {
                    if (keys_[i] === 'id') {
                        continue
                    }
                    let tr = $("<tr></tr>")
                    tr.append(`<th>${keys_[i]}</th>`)
                    for (let k in items) {
                        let value = items[k][keys_[i]]
                        if (keys_[i] === 'picture') {
                            value = 'http://' + window.location.host + value
                            tr.append(`<td><img src=${value} alt="image"></td>`)
                        } else {
                            tr.append(`<td>${value?value:'-'}</td>`)
                        }
                    }
                    $('#my-table tbody').append(tr)
                }
            }
            else {
                $("#my-table").append(`<p id="nullData">${result.msg}</p>`)
            }
        }})
    }
}



$(function() {
    $("#export").click(function(e){
        /*const table = $(this).prev('.table2excel');*/
        const table = $('#my-table')
        if(table && table.length && $('#nullData').length === 0){
            const preserveColors = (table.hasClass('table2excel_with_colors') ? true : false);
            $(table).table2excel({
                exclude: ".noExl",
                name: "Excel Document Name",
                filename: "myFileName" + new Date().toISOString().replace(/[\-\:\.]/g, "") + ".xls",
                fileext: ".xls",
                exclude_img: true,
                exclude_links: true,
                exclude_inputs: true,
                preserveColors: preserveColors
            });
        } else (
            alert("没有数据可以导出!!!")
        )
    });

});


