const { createApp } = Vue;

/* =========================================================
   1. スライド画像データの取得処理
   ========================================================= */
const slideDataElement = document.getElementById("slide-data");
let dbSlides = [];

if (slideDataElement) {
  try {
    dbSlides = JSON.parse(slideDataElement.textContent);
  } catch (e) {
    console.error("スライドデータの解析に失敗しました:", e);
  }
}

/* =========================================================
   2. イベントデータの取得処理
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
        artist1: item.artist1,
        artist2: item.artist2,
        artist3: item.artist3,
        artist4: item.artist4,
      };
    });
  } catch (e) {
    console.error("イベントデータの解析に失敗しました:", e);
    initialEvents = [];
  }
}

// Vue アプリケーションの定義
const app = createApp({
  data() {
    const now = new Date();
    const y = now.getFullYear();
    const m = now.getMonth() + 1; // 1-12

    // スライド画像の出し分け
    let finalHeroImages = [];
    
    if (dbSlides.length > 0) {
        finalHeroImages = dbSlides;
    } else {
        // DBがない場合のデフォルト画像
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
      
      heroImages: finalHeroImages,

      currentMonthDate: new Date(y, m - 1, 1),
      events: initialEvents,
      
      weekdays: ["月", "火", "水", "木", "金", "土", "日"],

      kaisetsu_profiles: [
        {
          path: STATIC_IMAGE_URLS.tateyama_kazuma,
          class1:"元ボートレーサー（大阪支部）",
          class2:"登録番号 2160",
          name: "立 山 一 馬 ",
          text: "アクアライブステーションのメイン解説者。楽しい解説をモットーとしています。",
        },
        {
          path: STATIC_IMAGE_URLS.tuda,
          class1:"元ボートレーサー（大阪支部）",
          class2:"登録番号 2717",
          name: "津 田 富士男",
          text: "現役時代は攻撃的なスタートまくりで大活躍。堅実な語り口が持ち味です。",
        },
        {
          path: STATIC_IMAGE_URLS.nozoe,
          class1:"元ボートレーサー（大阪支部）",
          class2:"登録番号 3555",
          name: "野 添 貴 裕",
          text: "近代ボートレース理論の伝導者。巧みな言語化能力で選手の心理を語ります。",
        },
        {
          path: STATIC_IMAGE_URLS.yamamoto_syuji,
          class1:"元ボートレーサー（滋賀支部）",
          class2:"登録番号 3633",
          name: "山 本 修 次",
          text: "国立大卒＞＞＞ボートレーサーという異色の経歴の持ち主。舟券予想の解を導きます。",
        },
      ],
      mc_profiles: [
        {
          path: STATIC_IMAGE_URLS.hamaguchi,
          class1: "司会者",
          class2:"",
          name:  "濱口くみ",
          text:  "巧みな話術でトークを盛り上げます。",
        },
        {
          path: STATIC_IMAGE_URLS.hoshino,
          class1:"司会者",
          class2:"",
          name: "星野あゆみ",
          text: "アナウンス力と親しみやすさを併せ持つ、優れた司会者です。",
        },      
        {
          path: STATIC_IMAGE_URLS.masuda,
          class1: "司会者",
          class2:"",
          name:  "益田あゆみ",
          text:  "アイドルから司会者とマルチに活躍中。",
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

    /* =========================================================
       ★修正ポイント: スマホリスト用イベント（過去日非表示対応）
       ========================================================= */
    monthEvents() {
      // 現在の日付を取得
      const now = new Date();
      const realYear = now.getFullYear();
      const realMonth = now.getMonth() + 1;
      const realDay = now.getDate();

      const out = [];
      for (const e of this.events) {
        const md = e.y && e.m && e.d ? e : this.parseDateParts(e.date);
        if (!md) continue;
        const yy = md.y ?? this.year;

        // 表示対象の月かチェック
        if (yy === this.year && md.m === this.month) {
            
            // ★追加ロジック: 
            // 「表示しているのが現在の月」かつ「日付が今日より前」ならリストに含めない
            if (this.year === realYear && this.month === realMonth) {
                if (md.d < realDay) {
                    continue; // 過去の日付はスキップ
                }
            }
            // (過去の月を見ている場合は履歴として全件表示されます)

            out.push({ ...e, y: yy, m: md.m, d: md.d });
        }
      }
      // 日付順 > 時間順にソート
      return out.sort(
        (a, b) =>
          a.d - b.d || String(a.time || "").localeCompare(String(b.time || ""))
      );
    },
    
    // PCカレンダー用データ（こちらは全日程を表示する）
    calendarDays() {
      const days = [];
      const firstDayOfWeek = new Date(this.year, this.month - 1, 1).getDay();
      const emptyCount = (firstDayOfWeek + 6) % 7; // 月曜始まり調整

      for (let i = 0; i < emptyCount; i++) {
        days.push({ date: "", events: [] });
      }

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
    // 曜日取得用
    getWeekday(y, m, d) {
        if (!y || !m || !d) return "";
        const date = new Date(y, m - 1, d);
        const dayIndex = date.getDay(); // 0=日, 1=月...
        const index = (dayIndex + 6) % 7; // 月曜始まりインデックス
        return this.weekdays[index];
    },

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

app.config.compilerOptions.delimiters = ["[[", "]]"];

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
    
    if (!("IntersectionObserver" in window)) {
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