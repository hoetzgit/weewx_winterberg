<!-- Rename this file to index_radar.inc 
See other example at https://github.com/poblabs/weewx-belchertown/issues/703 -->
<div id="tabs-container">
            <a name="webcam" href="https://www.beathis.ch/meteo/middle.jpg" target="_blank"><img src="https://www.beathis.ch/meteo/mobile.jpg"></a>
</div>

<script type="text/javascript">
jQuery(document).ready(function() {
    reloadWebcam(); // Force the cache on each load
    setInterval('reloadWebcam()', 300000); // 5 mins in millis
});

function reloadWebcam() {
    jQuery('#webcam img').each(function() {
        new_image_url = jQuery(this).attr('src').split('?')[0] + "?" + Math.floor(Math.random() * 999999999);
        jQuery(this).attr('src', new_image_url);
    });
}

jQuery('.tabs-menu a').click(function(event) {
    event.preventDefault();

    // Toggle active class on tab buttons
    jQuery(this).parent().addClass("active");
    jQuery(this).parent().siblings().removeClass("active");

    // display only active tab content
    var activeTab = jQuery(this).attr("href");
    jQuery('.tab-content').not(activeTab).css("display","none");
    jQuery(activeTab).fadeIn();

});
</script>

<style>
.dark .tabs-menu > li > a {
    padding: 0px 5px;
}

.dark .nav-tabs>li.active>a, .dark .nav-tabs>li.active>a:focus, .dark .nav-tabs>li.active>a:hover {
    color: #e5554e;
}

.active a {
    /* color:red; */
}

.tab-content {
    display:none;
}

.tabs-menu > li > a {
    padding: 0px 5px;
}

#radar {
    display:block;
}
</style>
