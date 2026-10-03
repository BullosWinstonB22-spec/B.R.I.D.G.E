// Optional Node.js Firebase Cloud Functions for B.R.I.D.G.E.
// Deploy with: cd functions && npm run deploy
import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
admin.initializeApp();

// Example: callable from the frontend to request a barangay document.
export const requestDocument = functions.https.onCall(async (data, context) => {
  if (!context.auth) throw new functions.https.HttpsError("unauthenticated", "Sign in first.");
  const { documentType, purpose } = data;
  const ref = admin.firestore().collection("documentRequests").doc();
  await ref.set({
    userId: context.auth.uid,
    documentType,
    purpose,
    status: "PENDING",
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
  });
  return { requestId: ref.id, status: "PENDING" };
});

// Example: Firestore-triggered notification when a document status changes.
export const onDocumentStatusChange = functions.firestore
  .document("documentRequests/{id}")
  .onUpdate(async (change) => {
    const before = change.before.data();
    const after = change.after.data();
    if (before?.status !== after?.status && after?.status === "READY") {
      functions.logger.info(`Document ${change.after.id} is ready for pickup.`);
      // TODO: send FCM / SMS notification to resident
    }
    return null;
  });
