import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className="hero hero--primary">
      <div className="container">
        <div className="row">
          <div className="col col--6">
            <h1 className="hero__title">
              Physical AI & Humanoid Robotics
            </h1>
            <p className="hero__subtitle">
              Explore the cutting-edge of robotics, covering topics like dynamics, control, perception, and learning for humanoid robots.
            </p>
            <div className="margin-top--lg">
              <Link
                className="button button--secondary button--lg"
                to="/signin">
                Sign In to Read
              </Link>
            </div>
          </div>
          <div className="col col--6">
            <div className="text--center">
              <img
                src={require('@site/static/img/robot-hero.png').default}
                alt="Humanoid Robot"
                className="hero-image"
                style={{
                  maxWidth: '100%',
                  height: 'auto',
                  borderRadius: '12px',
                  boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.1)',
                }}
              />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics Textbook">
      <HomepageHeader />
    </Layout>
  );
}