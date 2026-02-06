import Stripe from "stripe";
import { db } from "@redmed/db";
import { requireSession } from "@/lib/auth";
import { NextResponse } from "next/server";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "");

export async function POST() {
  const session = await requireSession();
  const user = await db.user.findUnique({ where: { authProviderId: session.authProviderId }, include: { subscriptions: true } });
  const subscription = user?.subscriptions.at(0);
  if (!user || !subscription) return NextResponse.json({ error: "not_found" }, { status: 404 });
  const portal = await stripe.billingPortal.sessions.create({ customer: subscription.stripeCustomerId, return_url: process.env.STRIPE_RETURN_URL ?? "" });
  return NextResponse.json({ url: portal.url });
}
