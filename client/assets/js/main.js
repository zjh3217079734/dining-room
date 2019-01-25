(function ($) {
    'use strict';

    /* Cart Currency Search toggle active */
    $(".header-cart a").on("click", function (e) {
        e.preventDefault();
        $(this).parent().find('.shopping-cart-content').slideToggle('medium');
    })

    /*--
    Menu Stick
    -----------------------------------*/
    var header = $('.transparent-bar');
    var win = $(window);

    win.on('scroll', function () {
        var scroll = win.scrollTop();
        if (scroll < 200) {
            header.removeClass('stick');
        } else {
            header.addClass('stick');
        }
    });

    /* jQuery MeanMenu */
    $('#mobile-menu-active').meanmenu({
        meanScreenWidth: "991",
        meanMenuContainer: ".mobile-menu-area .mobile-menu",
    });


    /* Slider active */
    $('.slider-active').owlCarousel({
        loop: true,
        nav: true,
        autoplay: false,
        autoplayTimeout: 5000,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        item: 1,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })

    /* Best selling active */
    $('.product-slider-active').owlCarousel({
        loop: true,
        nav: true,
        autoplay: false,
        autoplayTimeout: 5000,
        navText: ['<i class="ion-ios-arrow-back"></i>', '<i class="ion-ios-arrow-forward"></i>'],
        item: 3,
        margin: 30,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 2
            },
            992: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    })

    /* Best selling active */
    $('.related-product-active').owlCarousel({
        loop: true,
        nav: true,
        autoplay: false,
        autoplayTimeout: 5000,
        navText: ['<i class="ion-ios-arrow-back"></i>', '<i class="ion-ios-arrow-forward"></i>'],
        item: 4,
        margin: 30,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 3
            },
            992: {
                items: 3
            },
            1100: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    })



    /* Testimonial active */
    $('.testimonial-active').owlCarousel({
        loop: true,
        nav: false,
        autoplay: false,
        autoplayTimeout: 5000,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        item: 1,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })

    /* Brand logo active */
    $('.brand-logo-active').owlCarousel({
        loop: true,
        nav: false,
        autoplay: false,
        autoplayTimeout: 5000,
        item: 5,
        margin: 80,
        responsive: {
            0: {
                items: 1,
                margin: 0,
            },
            480: {
                items: 2,
                margin: 30,
            },
            768: {
                items: 4,
                margin: 30,
            },
            992: {
                items: 4,
                margin: 100,
            },
            1200: {
                items: 5
            }
        }
    })


    /*---------------------
        Countdown
    --------------------- */
    $('[data-countdown]').each(function () {
        var $this = $(this),
            finalDate = $(this).data('countdown');
        $this.countdown(finalDate, function (event) {
            $this.html(event.strftime('<span class="cdown day">%-D <p>Days</p></span> <span class="cdown hour">%-H <p>Hour</p></span> <span class="cdown minutes">%M <p>Min</p></span class="cdown second"> <span>%S <p>Sec</p></span>'));
        });
    });


    /*--------------------------
        ScrollUp
    ---------------------------- */
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-double-up"></i>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });


    /*---------------------
        Price slider
    --------------------- */
    var sliderrange = $('#slider-range');
    var amountprice = $('#amount');
    $(function () {
        sliderrange.slider({
            range: true,
            min: 0,
            max: 200,
            values: [0, 200],
            slide: function (event, ui) {
                amountprice.val("￥" + ui.values[0] + " - ￥" + ui.values[1]);
            }
        });
        amountprice.val("￥" + sliderrange.slider("values", 0) +
            " - ￥" + sliderrange.slider("values", 1));
    });

    /*---------------------
        Product dec slider
    --------------------- */
    $('.product-dec-slider').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        centerPadding: '60px',
        prevArrow: '<span class="product-dec-icon product-dec-prev"><i class="fa fa-angle-left"></i></span>',
        nextArrow: '<span class="product-dec-icon product-dec-next"><i class="fa fa-angle-right"></i></span>',
        responsive: [{
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 479,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            }
        ]
    });

    /*------ Wow Active ----*/
    new WOW().init();

    /* counterUp */
    $('.count').counterUp({
        delay: 10,
        time: 1000
    });

    /*----------------------------
        Cart Plus Minus Button
        购物车增减及小计功能函数
    ------------------------------ */
    var CartPlusMinus = $('.cart-plus-minus');

    CartPlusMinus.prepend('<div class="dec qtybutton">-</div>');
    CartPlusMinus.append('<div class="inc qtybutton">+</div>');
    $(".qtybutton").on("click", function () {
        var $button = $(this);
        var oldValue = $button.parent().find("input").val();
        if ($button.text() === "+") {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // 不允许小于零
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 1;
            }
        }
        //文本框赋值
        $button.parent().find("input").val(newVal);
        //取出单价
        var priceStr = $(this).parent(".cart-plus-minus").parent(".product-quantity").prev('.product-price-cart').find(".amount").html();
        // console.log(priceStr)
        var price = Number(priceStr.substring(1));
        //算小计
        var xiaoji = newVal * price
        //小计赋值
        $(this).parent(".cart-plus-minus").parent(".product-quantity").next(".product-subtotal").html("&yen;" + xiaoji);

        countItem();

    });
    /*----------------------------
   Cart remonve
   购物车删除
   
   ------------------------------ */
    $(".fa-times").click(function () {
        $(this).parent().parent().parent().remove()
        countItem();
    })
    /*----------------------------
  Cart note
  购物车备注
  ------------------------------ */
    var writeNote = false
    $(".fa-pencil").click(function () {
        writeNote = !writeNote
        //    window.writeNote = writeNote
        if (writeNote) {
            $(this).parent().parent('.product-remove').append("<input class='beizhu' type='text' style='font-size:6px' value='备注:'>")
        } else {
            $(this).parent().parent('.product-remove').find('.beizhu').remove()
        }

    })
    //    $(".fa-pencil").blur(function () {
    //        writeNote = false
    //    })
    /*----------------------------
        Cart count
        购物统计数量及总价函数
    ------------------------------ */

    function countItem() {
        var allPrice = 0;
        window.allPrice = allPrice
        var count = 0 // 总数
        $(".product-quantity").each(function () {
            // dxk();
            count +=
                Number($(this).find(".cart-plus-minus-box").val());
            // console.log(count)
            var priceStr = $(this).next(".product-subtotal").html();
            var priceNum = Number(priceStr.substring(1));
            allPrice += priceNum
            window.allPrice = allPrice
        })
        $("#dbcj").each(function () {
            if ($("input[name='dbcj']:checked").val() == "on") {
                allPrice += 20;
                // console.log(allPrice)
            }
        })
        $("#kpf").each(function () {
            if ($("input[name='kpf']:checked").val() == "on") {
                allPrice += 30;
            }
        })
        console.log(allPrice)
        $(".grand-totall-title span").html("&yen;" + allPrice);
        $(".grand-totall-number span").html(count);
        /*----------------------------
        Cart checkbox
        购物车单选框
        不要把问题想得太复杂,就是加或者还原
        ------------------------------ */
    }
    countItem();
    var isChicked = false
    var isChicked2 = false
    $("#dbcj").click(function () {
        isChicked = !isChicked
        if (isChicked) {
            countItem()
            // allPrice += 20;
            // console.log($("input[name='dbcj']:checked").val())
            // $(".grand-totall-title span").html("&yen;" + allPrice);
            // console.log(allPrice)
            // window.allPrice = allPrice
        } else {
            countItem()
            //    $(this).removeAttr("checked")
            // $(".grand-totall-title span").html("&yen;" + allPrice);
            // allPrice -= 20;
            // $(".grand-totall-title span").html("&yen;" + allPrice);
            // console.log(allPrice)
            // window.allPrice = allPrice

        }
    })
    $("#kpf").click(function () {
        // console.log(allPrice)
        isChicked2 = !isChicked2
        if (isChicked2) {
            countItem()
            // allPrice += 30;
            // console.log(allPrice)
            // window.allPrice = allPrice

            // $(".grand-totall-title span").html("&yen;" + allPrice);
        } else {
            countItem()
            //    $(this).removeAttr("checked")
            // $(".grand-totall-title span").html("&yen;" + allPrice);
            // allPrice -= 30;
            // $(".grand-totall-title span").html("&yen;" + allPrice);
            // window.allPrice = allPrice
            // console.log(allPrice)
        }
    })

    //显示限制输入字符method
    function textAreaChange(obj) {
        var $this = $(obj);
        var count_total = $this.next().children('span').text();
        var count_input = $this.next().children('em');
        var area_val = $this.val();
        if (area_val.len() > count_total) {
            area_val = autoAddEllipsis(area_val, count_total); //根据字节截图内容
            $this.val(area_val);
            count_input.text(0); //显示可输入数
        } else {
            count_input.text(count_total - area_val.len()); //显示可输入数
        }
    }
    //得到字符串的字节长度
    String.prototype.len = function () {
        return this.replace(/[^\x00-\xff]/g, "xx").length;
    };
    /*
     * 处理过长的字符串，截取并添加省略号
     * 注：半角长度为1，全角长度为2
     * pStr:字符串
     * pLen:截取长度
     * return: 截取后的字符串
     */
    function autoAddEllipsis(pStr, pLen) {
        var _ret = cutString(pStr, pLen);
        var _cutFlag = _ret.cutflag;
        var _cutStringn = _ret.cutstring;
        return _cutStringn;
    }
    /*
     * 取得指定长度的字符串
     * 注：半角长度为1，全角长度为2
     * pStr:字符串
     * pLen:截取长度
     * return: 截取后的字符串
     */
    function cutString(pStr, pLen) {
        // 原字符串长度
        var _strLen = pStr.length;
        var _tmpCode;
        var _cutString;
        // 默认情况下，返回的字符串是原字符串的一部分
        var _cutFlag = "1";
        var _lenCount = 0;
        var _ret = false;
        if (_strLen <= pLen / 2) {
            _cutString = pStr;
            _ret = true;
        }
        if (!_ret) {
            for (var i = 0; i < _strLen; i++) {
                if (isFull(pStr.charAt(i))) {
                    _lenCount += 2;
                } else {
                    _lenCount += 1;
                }
                if (_lenCount > pLen) {
                    _cutString = pStr.substring(0, i);
                    _ret = true;
                    break;
                } else if (_lenCount == pLen) {
                    _cutString = pStr.substring(0, i + 1);
                    _ret = true;
                    break;
                }
            }
        }
        if (!_ret) {
            _cutString = pStr;
            _ret = true;
        }
        if (_cutString.length == _strLen) {
            _cutFlag = "0";
        }
        return {
            "cutstring": _cutString,
            "cutflag": _cutFlag
        };
    }
    /*
     * 判断是否为全角
     *
     * pChar:长度为1的字符串
     * return: true:全角
     *         false:半角
     */
    function isFull(pChar) {
        if ((pChar.charCodeAt(0) > 128)) {
            return true;
        } else {
            return false;
        }
    }

    /*-------------------------------------
        Thumbnail Product activation
    --------------------------------------*/
    $('.thumb-menu').owlCarousel({
        loop: true,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        margin: 15,
        smartSpeed: 1000,
        nav: true,
        dots: false,
        responsive: {
            0: {
                items: 3,
                autoplay: true,
                smartSpeed: 300
            },
            576: {
                items: 2
            },
            768: {
                items: 3
            },
            1000: {
                items: 3
            }
        }
    })
    $('.thumb-menu a').on('click', function () {
        $('.thumb-menu a').removeClass('active');
    })


    /*---------------------
    shop grid list
    --------------------- */
    $('.view-mode li a').on('click', function () {
        var $proStyle = $(this).data('view');
        $('.view-mode li').removeClass('active');
        $(this).parent('li').addClass('active');
        $('.product-view').removeClass('product-grid product-list').addClass($proStyle);
    })

    /* blog gallery slider */
    $('.blog-gallery-slider').owlCarousel({
        loop: true,
        nav: true,
        autoplay: true,
        autoplayTimeout: 5000,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        navText: ['<i class="ion-chevron-left"></i>', '<i class="ion-chevron-right"></i>'],
        item: 1,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })

    /*--------------------------
        Product Zoom
	---------------------------- */
    $(".zoompro").elevateZoom({
        gallery: "gallery",
        galleryActiveClass: "active",
        zoomWindowWidth: 300,
        zoomWindowHeight: 100,
        scrollZoom: false,
        zoomType: "inner",
        cursor: "crosshair"
    });


    $('.testimonial-2-active').owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        items: 2,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            800: {
                items: 1
            },
            992: {
                items: 2
            },
            1024: {
                items: 2
            },
            1200: {
                items: 2
            },
            1400: {
                items: 2
            },
            1920: {
                items: 2
            }
        }
    });


    /* magnificPopup video popup */
    $('.video-popup').magnificPopup({
        type: 'iframe'
    });


})(jQuery);