import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';

function SignUpPage() {
  return (
    <Layout title="Sign Up" description="Create an account to access the Physical AI & Humanoid Robotics textbook">
      <div className={clsx('hero hero--primary')}>
        <div className="container">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <div className="text--center padding-vert--xl">
                <h1 className="hero__title">Sign Up</h1>
                <p className="hero__subtitle">
                  Create an account to access the Physical AI & Humanoid Robotics textbook
                </p>

                {/* Minimalist signup form */}
                <div style={{maxWidth: '400px', margin: '0 auto'}}>
                  <form>
                    <div className="margin-bottom--lg">
                      <input
                        type="text"
                        placeholder="Full name"
                        className="form-control"
                        style={{width: '100%', padding: '12px', borderRadius: '6px', border: '1px solid #ddd'}}
                      />
                    </div>
                    <div className="margin-bottom--lg">
                      <input
                        type="email"
                        placeholder="Email address"
                        className="form-control"
                        style={{width: '100%', padding: '12px', borderRadius: '6px', border: '1px solid #ddd'}}
                      />
                    </div>
                    <div className="margin-bottom--lg">
                      <input
                        type="password"
                        placeholder="Password"
                        className="form-control"
                        style={{width: '100%', padding: '12px', borderRadius: '6px', border: '1px solid #ddd'}}
                      />
                    </div>
                    <div className="margin-bottom--lg">
                      <input
                        type="password"
                        placeholder="Confirm password"
                        className="form-control"
                        style={{width: '100%', padding: '12px', borderRadius: '6px', border: '1px solid #ddd'}}
                      />
                    </div>
                    <div className="margin-bottom--lg">
                      <button
                        type="submit"
                        className="button button--primary button--lg"
                        style={{width: '100%'}}
                      >
                        Sign Up
                      </button>
                    </div>
                  </form>

                  <div className="text--center margin-top--lg">
                    <p>Already have an account? <a href="/signin">Sign in here</a></p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default SignUpPage;