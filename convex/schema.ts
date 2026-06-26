import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  analyses: defineTable({

    imageName: v.string(),

    totalGarments: v.number(),

    items: v.array(
      v.object({
        type: v.string(),
        fabric: v.string(),
        color: v.string(),
        confidence: v.number()
      })
    ),

    createdAt: v.number()

  })
}); 