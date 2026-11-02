import { RefractionFilter } from "@/components/RefractionFilter";
import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { PainPoints } from "@/components/PainPoints";
import { CoreRules } from "@/components/CoreRules";
import { Demo } from "@/components/Demo";
import { HowItWorks } from "@/components/HowItWorks";
import { Skills } from "@/components/Skills";
import { Install } from "@/components/Install";
import { Footer } from "@/components/Footer";
import { BottomNav } from "@/components/BottomNav";
import { BackToTop } from "@/components/BackToTop";
import { LangProvider, useI18n } from "@/i18n";

function Shell() {
  const { t } = useI18n();
  return (
    <>
      <a href="#main" className="skip-link">{t.skip}</a>
      <div className="bg-scene" aria-hidden="true" />
      <RefractionFilter />
      <Navbar />
      <div className="has-bottom-nav">
        <main id="main">
          <Hero />
          <PainPoints />
          <CoreRules />
          <Demo />
          <HowItWorks />
          <Skills />
          <Install />
        </main>
        <Footer />
      </div>
      <BottomNav />
      <BackToTop />
    </>
  );
}

export default function App() {
  return (
    <LangProvider>
      <Shell />
    </LangProvider>
  );
}
