/* ============================================================
   terminal theme for ECharts
   ------------------------------------------------------------
   规范来源：E:\UI知识库\design-specs\design-spec-recruit-analytics.md
   目标：全站图表统一为「深底 + 灰阶 + 单一强调色(#ffa800)」
   做法：1) 注册 term 主题并让 echarts.init 默认使用它
        2) 拦截实例 setOption，剥掉业务脚本里写死的彩色/渐变
           （地图 series 除外，其配色由 visualMap 控制）
   ============================================================ */
(function () {
    if (!window.echarts) return;

    var T = {
        accent: '#ffa800',
        strong: '#fafafa',
        text: '#b0b0b0',
        muted: '#7a7a7a',
        line: '#2b2b2b',
        split: '#242424',
        panel: '#242424',
        font: 'Consolas, "Courier New", monospace'
    };

    // 灰阶为主，仅第一个色位给强调色
    var PALETTE = [T.accent, '#cfcfcf', '#9c9c9c', '#6f6f6f', '#4d4d4d', '#3d3d3d'];

    var axisCommon = {
        axisLine: { show: true, lineStyle: { color: T.line } },
        axisTick: { show: false, lineStyle: { color: T.line } },
        axisLabel: { show: true, color: T.text, fontSize: 11 },
        splitLine: { show: true, lineStyle: { color: T.split } },
        splitArea: { show: false, areaStyle: { color: ['rgba(255,255,255,0.02)', 'rgba(255,255,255,0)'] } },
        nameTextStyle: { color: T.muted, fontSize: 11 }
    };

    echarts.registerTheme('term', {
        color: PALETTE,
        backgroundColor: 'transparent',
        textStyle: { color: T.text, fontFamily: T.font, fontSize: 11 },

        title: {
            textStyle: { color: T.strong, fontWeight: 600, fontSize: 14 },
            subtextStyle: { color: T.muted, fontSize: 11 }
        },
        legend: {
            textStyle: { color: T.text, fontSize: 11 },
            itemWidth: 12,
            itemHeight: 8
        },
        tooltip: {
            backgroundColor: T.panel,
            borderColor: T.line,
            borderWidth: 1,
            textStyle: { color: T.text, fontFamily: T.font, fontSize: 11 },
            axisPointer: {
                lineStyle: { color: T.line },
                crossStyle: { color: T.line },
                label: { backgroundColor: T.panel, color: T.text }
            }
        },
        axisPointer: {
            lineStyle: { color: T.line },
            crossStyle: { color: T.line },
            label: { backgroundColor: T.panel, color: T.text }
        },
        categoryAxis: axisCommon,
        valueAxis: axisCommon,
        logAxis: axisCommon,
        timeAxis: axisCommon,
        line: { itemStyle: { borderWidth: 2 }, lineStyle: { width: 2 }, symbolSize: 4, symbol: 'circle', smooth: false },
        bar: { itemStyle: { barBorderWidth: 0 } },
        pie: {
            itemStyle: { borderWidth: 0 },
            // 标签与图例重复且易重叠，统一交给图例表达
            label: { show: false },
            labelLine: { show: false },
            emphasis: { label: { show: false } }
        },
        radar: {
            symbolSize: 4,
            lineStyle: { width: 1.5 },
            // 雷达只保留描边，面积做淡填充，避免变成色块
            areaStyle: { opacity: 0.16 },
            axisName: { color: T.text, fontSize: 11 },
            splitLine: { lineStyle: { color: T.split } },
            splitArea: { show: false },
            axisLine: { lineStyle: { color: T.line } }
        }
    });

    /* ---------- 1. 剥除硬编码彩色 ---------- */
    // 业务脚本里大量出现 color: '#4e73df' / LinearGradient 等，主题无法覆盖，
    // 统一在 setOption 前递归删除 series 内的 color 字段，让调色板接管。
    function stripColor(node, depth) {
        if (!node || typeof node !== 'object' || depth > 8) return;
        if (Array.isArray(node)) {
            for (var i = 0; i < node.length; i++) stripColor(node[i], depth + 1);
            return;
        }
        for (var k in node) {
            if (!Object.prototype.hasOwnProperty.call(node, k)) continue;
            var v = node[k];
            if (k === 'color') {
                if (typeof v === 'string' || Array.isArray(v) || (v && v.colorStops)) delete node[k];
            } else if (v && typeof v === 'object') {
                stripColor(v, depth + 1);
            }
        }
    }

    function sanitize(option) {
        if (!option) return;
        if (Array.isArray(option)) {
            for (var i = 0; i < option.length; i++) sanitize(option[i]);
            return;
        }
        var series = option.series;
        if (!series) return;
        var arr = Array.isArray(series) ? series : [series];
        for (var j = 0; j < arr.length; j++) {
            var s = arr[j];
            if (!s || typeof s !== 'object') continue;
            // 地图/关系图配色由 visualMap 控制，跳过
            if (s.type === 'map' || s.type === 'geo' || s.type === 'graph') continue;
            stripColor(s, 0);
        }
    }

    function patchInstance(inst) {
        if (!inst || inst.__termPatched || typeof inst.setOption !== 'function') return inst;
        inst.__termPatched = true;
        var _setOption = inst.setOption;
        inst.setOption = function (option) {
            try { sanitize(option); } catch (e) { /* 配置异常时保持原样 */ }
            return _setOption.apply(this, arguments);
        };
        return inst;
    }

    /* ---------- 2. 默认主题注入 ---------- */
    var _init = echarts.init;
    echarts.init = function (dom, theme, opts) {
        if (theme === null || theme === undefined || theme === '') theme = 'term';
        return patchInstance(_init.call(echarts, dom, theme, opts));
    };
})();
