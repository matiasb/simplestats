$(function () {

    // hard-code color indices to prevent them from shifting as
    // series are turned on/off
    var i = 0;
    $.each(data, function(key, val) {
        val.color = i;
        ++i;
    });
    
    var options = {
        xaxis: { mode: "time", timeformat: "%b %d <br/> %H:%M" },
        selection: { mode: "x" },
        grid: { hoverable: true, },
        lines: { show: true, lineWidth: 1 },
        points: { show: true },
        crosshair: { mode: "x" }
    };

    function render_dataset(dataset){
        var plot = $.plot($("#placeholder"), dataset, options);

        var overview = $.plot($("#overview"), dataset, {
            series: {
                lines: { show: true, lineWidth: 1 },
                shadowSize: 0
            },
            xaxis: { ticks: [], mode: "time" },
            yaxis: { ticks: [], min: 0, autoscaleMargin: 0.1 },
            selection: { mode: "x" }
        });

        // now connect the two

        $("#placeholder").bind("plotselected", function (event, ranges) {
            // do the zooming
            plot = $.plot($("#placeholder"), dataset,
                        $.extend(true, {}, options, {
                            xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to }
                        }));

            // don't fire event on the overview to prevent eternal loop
            overview.setSelection(ranges, true);
        });

        $("#overview").bind("plotselected", function (event, ranges) {
            plot.setSelection(ranges);
        });
    }


    function plotAccordingToChoices() {
        var show_data = [];
        $('input.series-choice:checked').each(function () {
            var key = $(this).attr("name");
            if (key && data[key]){
                show_data.push(data[key]);
            }
        });

        render_dataset(show_data);
    }

    $('input.series-choice').click(plotAccordingToChoices);
    plotAccordingToChoices();

    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
            border: '1px solid #fdd',
            padding: '2px',
            'background-color': '#fee',
            opacity: 0.80
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $("#placeholder").bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));

        if (item) {
            if (previousPoint != item.dataIndex) {
                previousPoint = item.dataIndex;
                $("#tooltip").remove();
                var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2);
                showTooltip(item.pageX, item.pageY,
                item.series.label + ": " + y);
            }
        }else{
            $("#tooltip").remove();
            previousPoint = null;
        }
    });

    $('#reset').click(function (){
        plotAccordingToChoices();
        return false;
    });
});