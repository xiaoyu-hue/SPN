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

export default function App() {
  return (
    <>
      <div className="bg-scene" aria-hidden="true" />
      <RefractionFilter />
      <Navbar />
      <main>
        <Hero />
        <PainPoints />
        <CoreRules />
        <Demo />
        <HowItWorks />
        <Skills />
        <Install />
      </main>
      <Footer />
    </>
  );
}
