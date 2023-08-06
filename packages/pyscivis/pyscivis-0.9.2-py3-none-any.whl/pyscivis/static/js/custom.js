steps = [
            {
                setVisibility: function(){
                  after_elems = document.body.querySelectorAll(".fileinputbtn, .jstree-container-ul, .main-app");
                  after_elems.forEach(node=>{node.style.visibility="hidden"})
                },
                intro: "Welcome to a short introduction of \"pyscivis\". "+
                "Feel free to click at stuff inside the highlighted boxes at any point."

            },
            {
                intro: "You can navigate using the arrow-keys and close this tutorial by clicking outside or hitting \"ESC\""
            },
            {
                setVisibility: function(){
                  after_elems = document.body.querySelectorAll(".jstree-container-ul, .main-app");
                  after_elems.forEach(node=>{node.style.visibility="hidden"})
                },
                element_name: ".fileinputbtn",
                intro: "Here you can select a file to be displayed."
            },
            {
                setVisibility: function(){
                  after_elems = document.body.querySelectorAll(".main-app");
                  after_elems.forEach(node=>{node.style.visibility="hidden"})
                },
                element_name: ".jstree-container-ul",
                intro: "This is the tree-like structure of the chosen file. Click on a leaf make the app display the data."
            },
            {
                setVisibility: function(){
                  after_elems = document.body.querySelectorAll(".visible");
                  after_elems.forEach(node=>{node.style.visibility="visible"})
                },
                element_name: '.main-app',
                intro: "This is the main application window."
            },
            {
                element_name: '.image-figure',
                intro: "This is the image figure. It can visualize both images and k-spaces - depending on the data. "+
                       "If there is a red indicator in the bottom left corner of the image, the image is being downsampled."
            },
            {
                element_name: '.bk-toolbar',
                intro: 'This is the toolbar. It offer various tools to manipulate the image or show additional information.',
                position: 'top'
            },
            {
                element_name: '.bk-tool-icon-pan',
                intro: 'The Pan-tool. Quite straightforward. If active, you can pan around inside the image. First you need to zoom in though.',
                position: 'top'
            },
            {
                element_name: '.bk-tool-icon-wheel-zoom',
                intro: 'The Zoom-tool. You can use your mouse wheel to zoom in or out of the image. '+
                       'If downsampling is active it will automatically resample the image. Nice!',
                position: 'top'
            },
            {
                element_name: '.bk-tool-icon-tap-select',
                intro: 'The Tap-tool. If active, a tap on the image will cause the Profile-figures on the right to be updated.',
                position: 'top'
            },
            {
                element_name: '.bk-tool-icon-box-edit',
                intro: 'The Box-Edit-tool. With this, you can draw regions of interests (ROI\'s) in the shape of rectangles. ',
                position: 'top'
            },
            {
                element_name: '.bk-tool-icon-reset',
                intro: 'The Reset-tool restores the image\'s original bounds, e.g., if you zoom in, it will zoom out as far as possible. ',
                position: 'top'
            },
            {
                element_name: '.image-figure',
                intro: 'Try it. Activate the tool, then hold "SHIFT", click on the image and drag to draw a ROI. '+
                       'Instead of holding "SHIFT" you can also double-click.',
                position: 'top'
            },
            {
                element_name: '.bk-tool-icon-hover',
                intro: 'The Hover-tool. Hovering over the image will show you the value at your mouse position.',
                position: 'top'
            },
            {
                element_name: '.bk-toolbar',
                intro: 'Be aware that the Box-Edit-tool and the Tap-tool cannot be active at the same time.',
                position: 'top'
            },
            {
                element_name: '.palette',
                intro: "Over here you will find palette-related controls.."
            },
            {
                element_name: '.palette-select',
                intro: "This is the palette-selector, no need to explain it, just try it!"
            },
            {
                element_name: '.palette-size',
                intro: "Here you can reduce the palette-size. Think 8-bit and 16-bit image."+
                       "You might only notice changes once you go below 20."
            },
            {
                element_name: '.palette-window',
                intro: "Here you can change the min- and max-colors of the palette. All colors are adjusted."
            },
            {
                element_name: '.palette-slider',
                intro: "This slider is similar, but this time we are actually cutting every color past this slider-range off."
            },
            {
                element_name: '.fit-to-frame-toggle',
                intro: "By default the minimum and maximum of most ranges in this app are calculated over the entire dataset."
            },
            {
                element_name: '.fit-to-frame-toggle',
                intro: "However, it can be useful to get the minimum and maximum of only the current image. This is what this toggle is for."
            },
            {
                element_name: '.cbar-radios',
                intro: "You can also change the color-scale, linear or logarithmic."
            },
            {
                element_name: '.axes-selector',
                intro: "As we are often dealing with multi-dimensional data, changing "+
                       "axes to look at the data from a different perspective can be useful, too."
            },
            {
                element_name: '.statistics-table',
                intro: "This is the statistics table. Statistics of selected data (within the ROI) are displayed here. "+
                       "If no ROI exists, the entire image is evaluated."
            },
            {
                element_name: '.slider-column',
                intro: "These sliders can be used to zap through the dimensions."
            },
            {
                element_name: '.slider-column',
                intro: "You can tap the play button on the right to have a dimension be 'played back'."
            },
            {
                element_name: '.histogram-figure',
                intro: "The histogram accumulates all values into bins. "+
                       "The blue part is for the selected data, the white part is for the entire frame."
            },
            {
                element_name: '.profile-figures',
                intro: "All profile figures are displayed here, one for every dimension. They offer a look inside the data."
            },
            {
                element_name: '.bk-tabs-header',
                intro: "There's some more options, for example you can access the State-tab. "+
                       "The stuff in there allows easy sharing of plot states with your colleagues."
            },
            {
                element_name: '.bk-tabs-header',
                intro: "More about that in the user manual..."
            },
            {
                element_name: '.main-app',
                intro: "You can play around with the the app now, if you want."
            },
            {
                intro: "That's it! I'll gladly accept criticism, feedback and suggestions on GitHub."
            }
        ]

function getSteps() {
    var valid_steps = []
    for (index in steps){
        let step = steps[index]
        if ("element" in step){
            let exists = document.getElementsByClassName(step["element"].substring(1)).length > 0
            if (exists){
                valid_steps.push(step)
            }
        } else {
            valid_steps.push(step)
        }
    }
    return valid_steps
}

function setStep(step) {
    if (intro._currentStep == step-2){
        intro.goToStep(step)
    }
}

function startIntro() {
    $(".bokeh-intro button").click()
    intro = introJs();

    intro.onbeforechange(function(targetElement) {
        var cur_item = this._introItems[this._currentStep]
        if (cur_item.element_name){
            cur_item.element = document.querySelector(cur_item.element_name)
            cur_item.position = "top"
            cur_item.element.style.visibility = "visible"
        }

        backtrack = this._currentStep

        while (backtrack != 0){
        if (this._introItems[backtrack].setVisibility)
            this._introItems[backtrack].setVisibility()
            break
        }

        var state = window.intro_state
        if (state === undefined)
            return

        state.data = {"step": [this._currentStep]}
    });

    intro.onbeforeexit(function() {
        var state = window.intro_state
        if (state === undefined)
            return

        state.data = {"step": [-1]}
    })

    intro.setOptions({
        steps: steps
    });

    intro.start();
}

$(function(){
    $("#darkmodetoggle").on("click", function(){
        if ($(this).is(":checked")){
            $(".btn-darkmode button").click()
            //$.jstree.defaults.core.themes.name = "default-dark";
        }else{
            $(".btn-lightmode button").click()
            //$.jstree.defaults.core.themes.name = "default";
        }
    })
});