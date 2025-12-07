const { createApp } = Vue;

/* =========================================================
   修正ポイント1: スライド画像データの取得処理を追加
   ========================================================= */
// HTML側の {{ hero_images_data|json_script:"slide-data" }} からデータを取得
const slideDataElement = document.getElementById("slide-data");
let dbSlides = [];

if (slideDataElement) {
  try {
    dbSlides = JSON.parse(slideDataElement.textContent);
    console.log("DBからのスライド画像読み込み成功:", dbSlides);
  } catch (e) {
    console.error("スライドデータの解析に失敗しました:", e);
  }
}

/* =========================================================
   既存処理: カレンダー用データの取得（そのまま維持）
   ========================================================= */
const rawDataElement = document.getElementById("data-json");
let initialEvents = [];

if (rawDataElement) {
  try {
    const rawData = JSON.parse(rawDataElement.textContent);
    let nextId = 1;

    initialEvents = rawData.map((item) => {
      const [y, m, d] = item.day.split("-").map(Number);
      return {
        id: `db-${nextId++}`,
        y: y,
        m: m,
        d: d,
        title: item.title,
        time: item.time,
        artist: item.artist,
      };
    });
  } catch (e) {
    console.error("イベントデータの解析に失敗しました:", e);
    initialEvents = [];
  }
}

// 2. Vue インスタンスの data に変換後のデータを適用
const app = createApp({
  data() {
    const now = new Date();
    const y = now.getFullYear();
    const m = now.getMonth() + 1; // 1-12

    /* =========================================================
       修正ポイント2: スライド画像の出し分けロジック
       ========================================================= */
    // DBから画像が取れていればそれを使い、なければ従来の静的画像を使う
    let finalHeroImages = [];
    
    if (dbSlides.length > 0) {
        // DBデータを使用
        finalHeroImages = dbSlides;
    } else {
        // DBが空の場合は、既存のデフォルト画像を使用（フォールバック）
        // ※ STATIC_IMAGE_URLS は HTML内の script タグで定義されている前提
        finalHeroImages = [
            {
              url: STATIC_IMAGE_URLS.aqualivestation_1,
              title: "ボートレース住之江",
              subtitle: "公式Youtubeチャンネル",
            },
            {
              url: STATIC_IMAGE_URLS.aqualivestation_2,
              title: "ライブ配信中！",
              subtitle: "臨場感あふれる実況",
            },
        ];
    }

    return {
      isMenuOpen: false,
      currentSlide: 0,
      currentYear: y,
      loading: true,
      error: null,
      
      // ★ ここに決定したスライド画像リストをセット
      heroImages: finalHeroImages,

      currentMonthDate: new Date(y, m - 1, 1),
      // ⭐ データベースから変換したデータを代入
      events: initialEvents,

      profiles: [
        {
          path: STATIC_IMAGE_URLS.tateyama_kazuma,
          class1:"元ボートレーサー",
          class2:"登録番号 2160",
          name: "立 山 一 馬 ",
          text: "アクアライブステーションのメイン解説者。楽しい解説をモットーとしています。",
        },
        {
          path: STATIC_IMAGE_URLS.tuda,
          class1:"元ボートレーサー",
          class2:"登録番号 2717",
          name: "津 田 富士男",
          text: "紹介文",
        },
        {
          path: STATIC_IMAGE_URLS.nozoe,
          class1:"元ボートレーサー",
          class2:"登録番号 3555",
          name: "野 添 貴 裕",
          text: "紹介文",
        },
        {
          path: STATIC_IMAGE_URLS.yamamoto_syuji,
          class1:"元ボートレーサー",
          class2:"登録番号 3633",
          name: "山 本 修 次",
          text: "紹介文",
        },
        {
          path: STATIC_IMAGE_URLS.hamaguchi,
          class1: "司会者",
          class2:"",
          name:  "濱口くみ",
          text:  "紹介文",
        },
                {
          path: STATIC_IMAGE_URLS.hoshino,
          class1:"司会者",
          class2:"",
          name: "星野あゆみ",
          text: "紹介文",
        },
                
                {
          path: STATIC_IMAGE_URLS.masuda,
          class1: "司会者",
          class2:"",
          name:  "益田あゆみ",
          text:  "紹介文",
        },
      ],
    };
  },
  computed: {
    year() {
      return this.currentMonthDate.getFullYear();
    },
    month() {
      return this.currentMonthDate.getMonth() + 1;
    }, // 1-12
    daysInMonth() {
      return new Date(this.year, this.month, 0).getDate();
    },
    monthEvents() {
      const out = [];
      for (const e of this.events) {
        const md = e.y && e.m && e.d ? e : this.parseDateParts(e.date);
        if (!md) continue;
        const yy = md.y ?? this.year;
        if (yy === this.year && md.m === this.month)
          out.push({ ...e, y: yy, m: md.m, d: md.d });
      }
      return out.sort(
        (a, b) =>
          a.d - b.d || String(a.time || "").localeCompare(String(b.time || ""))
      );
    },
    calendarDays() {
      const days = [];
      for (let d = 1; d <= this.daysInMonth; d++) {
        const dayEvents = this.events
          .filter((e) => {
            const md = e.y && e.m && e.d ? e : this.parseDateParts(e.date);
            if (!md) return false;
            const yy = md.y ?? this.year;
            return yy === this.year && md.m === this.month && md.d === d;
          })
          .map((e) => {
            const md = e.y && e.m && e.d ? e : this.parseDateParts(e.date);
            return { ...e, y: md.y ?? this.year, m: md.m, d: md.d };
          });
        days.push({ date: `${d}`, events: dayEvents });
      }
      return days;
    },
  },
  methods: {
    parseDateParts(input) {
      if (typeof input !== "string") return null;
      let m = input.match(/^(\d{4})-(\d{2})-(\d{2})$/);
      if (m) return { y: +m[1], m: +m[2], d: +m[3] };
      m = input.match(/^(\d{1,2})\/(\d{1,2})/);
      if (m) return { y: this.year, m: +m[1], d: +m[2] };
      return null;
    },

    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.heroImages.length;
    },
    prevSlide() {
      this.currentSlide =
        (this.currentSlide - 1 + this.heroImages.length) %
        this.heroImages.length;
    },
    async goMonth(offset) {
      const y = this.currentMonthDate.getFullYear();
      const m = this.currentMonthDate.getMonth();
      this.currentMonthDate = new Date(y, m + offset, 1);
    },
    goToday() {
      const now = new Date();
      this.currentMonthDate = new Date(now.getFullYear(), now.getMonth(), 1);
    },
  },
  async mounted() {
    setInterval(this.nextSlide, 5000);
  },
});

/* Vue 3 デリミタ */
app.config.compilerOptions.delimiters = ["[[", "]]"];

/* フェードイン（ループ対応） */
app.directive("reveal", {
  mounted(el, binding) {
    el.classList.add("reveal");
    const once = !!binding?.modifiers?.once || !!binding?.value?.once;
    const delay = binding?.value?.delay;
    const enter =
      typeof binding?.value?.enter === "number" ? binding.value.enter : 0.2;
    const exit =
      typeof binding?.value?.exit === "number" ? binding.value.exit : 0.0;
    const rootMargin = binding?.value?.rootMargin ?? "0px 0px -10% 0px";
    if (typeof delay === "number") el.style.transitionDelay = delay + "ms";
    // ★ ここでサポートチェック
    if (!("IntersectionObserver" in window)) {
      // 対応していないブラウザでは、最初から表示して終わり
      el.classList.add("is-visible");
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          const ratio = entry.intersectionRatio ?? 0;
          if (entry.isIntersecting && ratio >= enter) {
            el.classList.add("is-visible");
            if (once) io.unobserve(el);
          } else if (!once && ratio <= exit) {
            el.classList.remove("is-visible");
          }
        });
      },
      { threshold: [exit, enter], rootMargin }
    );

    el._io = io;
    io.observe(el);
  },
  unmounted(el) {
    el._io?.disconnect();
  },
});

app.mount("#app");