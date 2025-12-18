import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function LandingPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-12 px-4 py-12 md:max-w-5xl md:space-y-16 md:py-16">
      {/* Hero */}
      <section className="space-y-4 text-center">
        <h1 className="text-3xl font-semibold tracking-tight md:text-4xl">
          Analytics That Drive Growth
        </h1>
        <p className="mx-auto max-w-2xl text-muted-foreground">
          Wood Analytics helps businesses unlock insights with custom data
          strategy, scalable pipelines, actionable dashboards, and modern AI
          tools.
        </p>
        <div className="flex justify-center gap-3">
          <Button
            size="lg"
            onClick={() =>
              document
                .getElementById("contact")
                ?.scrollIntoView({ behavior: "smooth" })
            }
          >
            Work With Us
          </Button>
        </div>
      </section>

      {/* About */}
      <section id="about" className="space-y-3 text-center">
        <h2 className="text-2xl font-semibold tracking-tight">About Us</h2>
        <p className="mx-auto max-w-3xl text-muted-foreground">
          We are a data and AI consulting firm specializing in turning complex
          data into clear strategies. With expertise in SQL, Python, dbt, and
          modern data platforms, we help teams build and implement analytics and
          AI tools that unlock insights and drive growth.
        </p>
      </section>

      {/* Services */}
      <section id="services" className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight text-center">
          Our Services
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          <Card className="h-full">
            <CardHeader className="pb-2 text-center">
              <CardTitle className="text-base">Data Engineering</CardTitle>
            </CardHeader>
            <CardContent className="pt-0 text-sm text-muted-foreground text-center">
              Build scalable pipelines with dbt, SQL, and modern cloud
              platforms.
            </CardContent>
          </Card>

          <Card className="h-full">
            <CardHeader className="pb-2 text-center">
              <CardTitle className="text-base">Analytics &amp; BI</CardTitle>
            </CardHeader>
            <CardContent className="pt-0 text-sm text-muted-foreground text-center">
              Custom dashboards in Power BI &amp; Tableau to track the metrics
              that matter.
            </CardContent>
          </Card>

          <Card className="h-full">
            <CardHeader className="pb-2 text-center">
              <CardTitle className="text-base">Predictive Modeling</CardTitle>
            </CardHeader>
            <CardContent className="pt-0 text-sm text-muted-foreground text-center">
              Leverage advanced analytics and machine learning for smarter
              decisions.
            </CardContent>
          </Card>

          <Card className="h-full">
            <CardHeader className="pb-2 text-center">
              <CardTitle className="text-base">
                AI Tools &amp; Implementation
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-0 text-sm text-muted-foreground text-center">
              Build and deploy AI solutions that integrate seamlessly with your
              workflows.
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Proven Metrics */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight text-center">
          Proven Delivery Metrics
        </h2>
        <div className="grid gap-4 md:grid-cols-4">
          <MetricCard
            label="Industry Experience"
            value="10+ yrs"
            description="Analytics and data strategy across finance, SaaS, and consulting."
          />
          <MetricCard
            label="Implementation Timeline"
            value="2–4 wks"
            description="From kickoff to first working deliverable."
          />
          <MetricCard
            label="Query Optimization"
            value="3–5×"
            description="Average runtime improvement after tuning SQL."
          />
          <MetricCard
            label="AI Projects"
            value="10+"
            description="Delivered AI tool builds and implementation pilots."
          />
        </div>
      </section>

      {/* Why Us */}
      <section id="why-us" className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight text-center">
          Why Wood Analytics
        </h2>
        <p className="mx-auto max-w-3xl text-center text-sm text-muted-foreground">
          We combine real-world GTM expertise with modern data engineering to
          deliver decision-ready analytics fast.
        </p>
        <div className="grid gap-4 md:grid-cols-2">
          <BulletCard
            title="Business-First, Not Tool-First"
            items={[
              "Start with goals and KPIs.",
              "Design the minimal stack that achieves them.",
            ]}
          />
          <BulletCard
            title="Modern Stack Expertise"
            items={[
              "dbt, Postgres/Snowflake, FastAPI, HTMX.",
              "Production-ready CI/CD and observability.",
            ]}
          />
          <BulletCard
            title="Dashboards Executives Use"
            items={[
              "Clear narratives and curated metrics.",
              "Governance that leadership trusts.",
            ]}
          />
          <BulletCard
            title="Repeatable Playbooks"
            items={[
              "Templates for ingestion, modeling, and visualization.",
              "Deliver value in days, not months.",
            ]}
          />
          <BulletCard
            title="End-to-End Ownership"
            items={[
              "Data contracts, tests, alerts, and cost controls.",
              "No loose ends between teams.",
            ]}
          />
          <BulletCard
            title="Transparent Engagements"
            items={[
              "Fixed-scope packages and clear timelines.",
              "Weekly progress demos with stakeholders.",
            ]}
          />
        </div>
      </section>

      {/* Tech Stack */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight text-center">
          Tech Stack
        </h2>
        <p className="mx-auto max-w-3xl text-center text-sm text-muted-foreground">
          We choose proven, modern tools that balance speed, reliability, and
          cost—so you get maintainable analytics with business impact.
        </p>
        <div className="grid gap-4 md:grid-cols-2">
          <StackCard
            title="Data Layer"
            description="Durable storage and warehouses sized to your workload."
            tools={["Postgres", "Snowflake", "S3 (data lake)"]}
          />
          <StackCard
            title="Ingestion & APIs"
            description="Secure services and lightweight interactivity."
            tools={["FastAPI", "HTMX", "Python"]}
          />
          <StackCard
            title="Transformation & Modeling"
            description="Versioned SQL models and tested pipelines."
            tools={["dbt", "SQL", "Pydantic"]}
          />
          <StackCard
            title="Analytics & BI"
            description="Decision-ready dashboards for teams and leadership."
            tools={["Power BI", "Tableau", "Plotly"]}
          />
          <StackCard
            title="ML & Experimentation"
            description="Forecasting, attribution, and uplift with tracking."
            tools={["scikit-learn", "MLflow", "Causal Inference"]}
          />
          <StackCard
            title="AI & Automation"
            description="Practical AI tools tailored to your use cases."
            tools={["LLMs", "LangChain", "Custom APIs"]}
          />
        </div>
        <p className="text-center text-xs text-muted-foreground">
          Infrastructure is right-sized to your budget. CI/CD, tests, and
          documentation included.
        </p>
      </section>

      {/* How We Work */}
      <section className="space-y-4 text-center">
        <h2 className="text-2xl font-semibold tracking-tight">How We Work</h2>
        <p className="mx-auto max-w-3xl text-sm text-muted-foreground">
          A simple, proven process to help you unlock value from data.
        </p>
        <div className="grid gap-4 md:grid-cols-3">
          <StepCard
            step="1"
            title="Discover"
            description="Assess your current data landscape and define goals."
          />
          <StepCard
            step="2"
            title="Build"
            description="Engineer pipelines, models, and dashboards tailored to you."
          />
          <StepCard
            step="3"
            title="Scale"
            description="Enable long-term value through automation and insights."
          />
        </div>
      </section>

      {/* Contact / CTA */}
      <section id="contact" className="space-y-3 text-center">
        <h2 className="text-2xl font-semibold tracking-tight">
          Let’s Build Smarter Data &amp; AI Solutions Together
        </h2>
        <p className="mx-auto max-w-2xl text-muted-foreground">
          Ready to transform your data into impact? Schedule a consultation to
          discuss your use case.
        </p>
        <Button size="lg">Schedule a Consultation →</Button>
      </section>
    </div>
  );
}

function MetricCard(props: {
  label: string;
  value: string;
  description: string;
}) {
  return (
    <Card className="h-full">
      <CardHeader className="pb-1 text-center">
        <span className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
          {props.label}
        </span>
      </CardHeader>
      <CardContent className="space-y-1 pt-0 text-center">
        <div className="text-2xl font-semibold">{props.value}</div>
        <p className="text-xs text-muted-foreground">{props.description}</p>
      </CardContent>
    </Card>
  );
}

function BulletCard(props: { title: string; items: string[] }) {
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-base">{props.title}</CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <ul className="space-y-1.5 text-sm text-muted-foreground">
          {props.items.map((item) => (
            <li key={item}>• {item}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

function StackCard(props: {
  title: string;
  description: string;
  tools: string[];
}) {
  return (
    <Card className="h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-base">{props.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 pt-0">
        <p className="text-sm text-muted-foreground">{props.description}</p>
        <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
          {props.tools.map((tool) => (
            <span
              key={tool}
              className="rounded-full border px-2 py-0.5 text-[0.7rem]"
            >
              {tool}
            </span>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function StepCard(props: {
  step: string;
  title: string;
  description: string;
}) {
  return (
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center gap-3 pb-2">
        <div className="flex h-7 w-7 items-center justify-center rounded-full border text-xs font-medium">
          {props.step}
        </div>
        <CardTitle className="text-base">{props.title}</CardTitle>
      </CardHeader>
      <CardContent className="pt-0 text-sm text-muted-foreground">
        {props.description}
      </CardContent>
    </Card>
  );
}
