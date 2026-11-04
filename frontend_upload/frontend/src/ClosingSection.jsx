
import "./ClosingSection.css";

export default function ClosingSection() {
  return (
    <footer className="eco-ending" id="closing-section">
      <div className="eco-ending-inner">

        <div className="eco-ending-top">
          <a className="eco-brand" href="#overview">
            <span className="eco-brand-icon">↻</span>
            <span className="eco-brand-name">
              EcoSort <span>AI</span>
              <small>E-WASTE INTELLIGENCE</small>
            </span>
          </a>

          <div className="eco-status">
            <span className="eco-status-dot" />
            A SMALL STEP TOWARDS A GREENER FUTURE
          </div>
        </div>

        <div className="eco-ending-main">
          <div className="eco-ending-copy">
            <div className="eco-kicker">
              YOUR DEVICE. ITS NEXT CHAPTER.
            </div>

            <h2>
              Don't waste
              <br />
              <span>its potential.</span>
            </h2>

            <p className="eco-ending-description">
              That old phone, laptop, or gadget could still have
              a purpose. Find a smarter next step — repair it,
              reuse it, donate it, or recycle it responsibly.
            </p>

            <a href="#analyze" className="eco-primary-button">
              Find your device's next step
              <span>↗</span>
            </a>

            <div className="eco-ending-note">
              <span>✓</span>
              Better decisions start with one device.
            </div>
          </div>

          <div className="eco-ending-visual" aria-hidden="true">
            <div className="eco-visual-orbit orbit-one" />
            <div className="eco-visual-orbit orbit-two" />

            <div className="eco-visual-center">
              <span>↻</span>
              <small>GIVE TECH<br />A SECOND LIFE</small>
            </div>

            <div className="eco-float-card float-phone">
              <span className="eco-float-icon">▯</span>
              <span>
                <strong>Repair</strong>
                <small>Keep it useful</small>
              </span>
            </div>

            <div className="eco-float-card float-leaf">
              <span className="eco-float-icon">✳</span>
              <span>
                <strong>Reuse</strong>
                <small>Pass it forward</small>
              </span>
            </div>

            <div className="eco-float-card float-recycle">
              <span className="eco-float-icon">♻</span>
              <span>
                <strong>Recycle</strong>
                <small>Dispose responsibly</small>
              </span>
            </div>

            <span className="eco-decoration deco-one">✦</span>
            <span className="eco-decoration deco-two">✳</span>
          </div>
        </div>

        <div className="eco-ending-bottom">
          <div>
            <strong>EcoSort <span>AI</span></strong>
            <p>Smarter choices. Less e-waste.</p>
          </div>

          <a className="eco-back-top" href="#overview">
            Back to top <span>↑</span>
          </a>
        </div>

      </div>
    </footer>
  );
}
