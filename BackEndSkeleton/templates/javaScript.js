<!-- Should be in a seperate file -->
  <script type="text/javascript">
    function toggle_visibility(id) {
        var e = document.getElementById(id);
        if(e.style.visibility == 'visible')
            e.style.visibility = 'hidden'
        else
            e.style.visibility = 'visible'
    }

    function toggle_block(id) {
        var e = document.getElementById(id);
        if (e.style.display == 'block')
            e.style.display = 'none'
        else
            e.style.display = 'block'
    }

    function hide(id) {
      var e = document.getElementById(id);
      e.style.visibility='hidden'
      e.style.display='none'
    }
 
  </script>