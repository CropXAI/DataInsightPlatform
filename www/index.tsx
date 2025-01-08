import { page } from "fresh";
import VERSIONS from "../../versions.json" with { type: "json" };
import Footer from "../components/Footer.tsx";
import Header from "../components/Header.tsx";

import { Hero } from "../components/homepage/Hero.tsx";

import { define } from "../utils/state.ts";
import { postsData } from "../data/postsData.ts";
import { NewsCard } from "../components/NewsCard.tsx";
import { FancyLink } from "../components/FancyLink.tsx";

import OrdersIsland from "../islands/OrdersIsland.tsx";
import SearchDialog from "../islands/SearchDialog.tsx";

export const handler = define.handlers({
  GET(ctx) {
    const { req } = ctx;
    const accept = req.headers.get("accept");
    const userAgent = req.headers.get("user-agent");
    if (userAgent?.includes("Deno/") && !accept?.includes("text/html")) {
      const path = `https://deno.land/x/fresh@${VERSIONS[0]}/init.ts`;
      return new Response(`Redirecting to ${path}`, {
        headers: { "Location": path },
        status: 307,
      });
    }

    ctx.state.title = "РОСТ Х - Множитель роста";
    ctx.state.description =
      "Начните рост с теста микробиома почвы по спец. цене 7999 р 6749 р Узнайте подробнее →";
    /* ctx.state.ogImage = new URL(asset("/og-image.webp"), ctx.url).href; */

    return page();
  },
  async POST(ctx) {
    const headers = new Headers();
    const form = await ctx.req.formData();
    const treat = form.get("treat") as string | null;

    if (treat) {
      headers.set("location", `/thanks?vote=${encodeURIComponent(treat)}`);
    } else {
      headers.set("location", "/thanks?error=missing_vote");
    }

    return new Response(null, {
      status: 303,
      headers,
    });
  },
});

export default define.page<typeof handler>(function MainPage(props) {
  const origin = `${props.url.protocol}//${props.url.host}`;

  return (
    <div class="flex flex-col min-h-screen">
      <div class="bg-transparent flex flex-col relative z-10">
        {/* <HelloBar /> */}

        <Header title="" active="/" />
        {/* <SearchDialog /> */}
      </div>
      <div class="flex flex-col -mt-20 relative">
        <Hero origin={origin} />
        <div class="flex flex-col min-h-screen">
          <div class="bg-transparent flex flex-col relative">
            {postsData.posts.length > 0 && (
              <section class="flex flex-col gap-4 mb-8 md:mb-9 mr-4 ml-4 md:mr-16 md:ml-16">
                <h2
                  class="text-3xl md:text-4xl mb-4 md:mb-8 font-semibold text-center"
                  id="products"
                >
                  Продукты
                </h2>
                <OrdersIsland />
              </section>
            )}
          </div>

          {postsData.posts.length > 0 && (
            <section class="flex flex-col gap-4 mb-16 md:mb-32 mr-4 ml-4 md:mr-16 md:ml-16">
              <h2 class="text-3xl md:text-4xl mb-4 md:mb-8 font-semibold text-center">
                Что нужно знать об исследовании плодородия почвы в 2025?{"  "}
              </h2>
              <ul class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-8">
                {postsData?.posts?.slice(3, 11).map((post) => (
                  <NewsCard
                    key={post.title}
                    image={post.image}
                    title={post.title}
                    description={post.description}
                    url={post.url}
                    modalText={post.modalText}
                  />
                ))}
              </ul>
              {
                /* <a
                                href="https://deno.com/blog?tag=jsr"
                                class="underline block mt-4 w-full text-center"
                            >
                                More JSR updates{" "}
                                <span aria-hidden="true">&rsaquo;</span>
                            </a> */
              }
            </section>
          )}
        </div>
        {/*  <Simple /> */}
        {
          /*  <RenderingSection />
        <IslandsSection />
        <FormsSection />  */
        }
        {
          /* <PartialsSection />
        <SocialProof />
        <DenoSection /> */
        }
        {/* <CTA /> */}
      </div>
      <FancyLink
        href="https://chat.cropxai.com"
        class="mx-auto mb-[6rem] md:mb-[8rem]"
      >
        Начало роста
      </FancyLink>
      <Footer class="!mt-0" />
    </div>
  );
});
